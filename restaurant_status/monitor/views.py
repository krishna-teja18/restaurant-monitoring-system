import csv
import uuid
import pytz
import logging
from datetime import datetime, timedelta
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from monitor.models import StoreStatus, BusinessHours, StoreTimezone, Report
from django.db.models import Max
from io import StringIO
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)

def trigger_report(request):
    report_id = str(uuid.uuid4())
    report = Report.objects.create(report_id=report_id, status="Running")
    
    logger.info(f"Report generation started with report_id: {report_id}")
    print(f"Report generation started with report_id: {report_id}")

    max_timestamp = StoreStatus.objects.aggregate(Max('timestamp_utc'))['timestamp_utc__max']
    generate_report(report, max_timestamp)
    
    logger.info(f"Report generation completed with report_id: {report_id}")
    print(f"Report generation completed with report_id: {report_id}")

    return JsonResponse({"report_id": report_id})

def generate_report(report, max_timestamp):
    stores = StoreStatus.objects.values_list('store_id', flat=True).distinct()
    print(f"Found {len(stores)} distinct stores")

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['store_id', 'uptime_last_hour', 'uptime_last_day', 'uptime_last_week',
                     'downtime_last_hour', 'downtime_last_day', 'downtime_last_week'])

    batch_size = 100
    store_batches = [stores[i:i + batch_size] for i in range(0, len(stores), batch_size)]

    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_batch = {executor.submit(process_store_batch, writer, batch, max_timestamp): batch for batch in store_batches}

        count = 0
        for future in as_completed(future_to_batch):
            batch = future_to_batch[future]
            try:
                future.result()
                count += len(batch)
                logger.info(f"Processed {count} stores so far")
                print(f"Processed {count} stores so far")
            except Exception as e:
                logger.error(f"Error processing batch {batch}: {e}")
                print(f"Error processing batch {batch}: {e}")

    report_csv = output.getvalue()
    output.close()
    print(f"Generated CSV content length: {len(report_csv)}")
    
    if len(report_csv) > 0:
        report.csv_file.save(f"{report.report_id}.csv", StringIO(report_csv))
        report.status = "Complete"
    else:
        logger.error("No data was written to the CSV file")
        print("No data was written to the CSV file")
        report.status = "Failed"
    
    report.save()

def process_store_batch(writer, store_batch, max_timestamp):
    store_timezones = StoreTimezone.objects.filter(store_id__in=store_batch)
    business_hours = BusinessHours.objects.filter(store_id__in=store_batch)

    store_timezone_dict = {timezone.store_id: timezone for timezone in store_timezones}
    business_hours_dict = {}
    
    for bh in business_hours:
        if bh.store_id not in business_hours_dict:
            business_hours_dict[bh.store_id] = []
        business_hours_dict[bh.store_id].append(bh)

    rows = []
    for store in store_batch:
        timezone_obj = store_timezone_dict.get(store, None)
        if timezone_obj:
            timezone_str = timezone_obj.timezone_str
        else:
            timezone_str = 'America/Chicago'
            logger.warning(f"No timezone found for store_id {store}. Using default timezone 'America/Chicago'")

        store_tz = pytz.timezone(timezone_str)

        uptime_last_hour, downtime_last_hour = calculate_uptime_downtime(store, max_timestamp, store_tz, timedelta(hours=1))
        uptime_last_day, downtime_last_day = calculate_uptime_downtime(store, max_timestamp, store_tz, timedelta(days=1))
        uptime_last_week, downtime_last_week = calculate_uptime_downtime(store, max_timestamp, store_tz, timedelta(weeks=1))

        rows.append([store, uptime_last_hour, uptime_last_day, uptime_last_week,
                     downtime_last_hour, downtime_last_day, downtime_last_week])

    if rows:
        writer.writerows(rows)
        logger.info(f"Batch written to CSV. Number of rows: {len(rows)}")
        print(f"Batch written to CSV. Number of rows: {len(rows)}")
    else:
        logger.warning(f"No rows to write for store batch: {store_batch}")
        print(f"No rows to write for store batch: {store_batch}")


def calculate_uptime_downtime(store, max_timestamp, store_tz, time_delta):
    end_time = max_timestamp
    start_time = max_timestamp - time_delta

    end_time_local = end_time.astimezone(store_tz)
    start_time_local = start_time.astimezone(store_tz)

    statuses = StoreStatus.objects.filter(
        store_id=store,
        timestamp_utc__gte=start_time,
        timestamp_utc__lte=end_time
    ).order_by('timestamp_utc')

    business_hours = BusinessHours.objects.filter(
        store_id=store,
        day__in=[start_time_local.weekday(), end_time_local.weekday()]
    )

    if not business_hours.exists():
        return time_delta.total_seconds() / 60, 0

    uptime = timedelta()
    downtime = timedelta()
    current_status = None
    current_start = None

    for status in statuses:
        status_time = status.timestamp_utc.astimezone(store_tz)

        if current_status is None:
            current_status = status.status
            current_start = status_time

        if current_status != status.status:
            business_time = calculate_business_time(current_start, status_time, business_hours, store_tz)
            if current_status == 'active':
                uptime += business_time
            else:
                downtime += business_time

            current_status = status.status
            current_start = status_time

    if current_status:
        business_time = calculate_business_time(current_start, end_time_local, business_hours, store_tz)
        if current_status == 'active':
            uptime += business_time
        else:
            downtime += business_time

    return round(uptime.total_seconds() / 60, 2), round(downtime.total_seconds() / 60, 2)

def calculate_business_time(start_time, end_time, business_hours, store_tz):
    business_time = timedelta()

    start_time = start_time.astimezone(store_tz)
    end_time = end_time.astimezone(store_tz)

    for business_hour in business_hours:
        day_start = datetime.combine(start_time.date(), business_hour.start_time_local).astimezone(store_tz)
        day_end = datetime.combine(start_time.date(), business_hour.end_time_local).astimezone(store_tz)

        if start_time < day_start:
            start_time = day_start
        if end_time > day_end:
            end_time = day_end

        if start_time < end_time:
            business_time += end_time - start_time

    return business_time

def get_report(request, report_id):
    report = get_object_or_404(Report, report_id=report_id)
    if report.status == "Running":
        return JsonResponse({"status": "Running"})
    else:
        response = HttpResponse(report.csv_file, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{report.report_id}.csv"'
        return response
