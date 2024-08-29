import csv
from django.core.management.base import BaseCommand
from django.utils import timezone
from monitor.models import StoreStatus, BusinessHours, StoreTimezone
from datetime import datetime
import pytz

class Command(BaseCommand):
    help = 'Load data from CSV files'

    def handle(self, *args, **kwargs):
        self.load_store_status()
        self.load_business_hours()
        self.load_store_timezone()

    def load_store_status(self):
        batch_size = 1000
        store_status_entries = []
        with open('store status.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for i, row in enumerate(reader):
                store_id = row[0]
                status = row[1]
                timestamp_utc = self.parse_timestamp(row[2], store_id)
                store_status_entries.append(StoreStatus(
                    store_id=store_id,
                    status=status,
                    timestamp_utc=timestamp_utc
                ))
                
                if len(store_status_entries) >= batch_size:
                    StoreStatus.objects.bulk_create(store_status_entries)
                    print(f"Inserted {i + 1} rows into StoreStatus")
                    store_status_entries = []

            if store_status_entries:
                StoreStatus.objects.bulk_create(store_status_entries)
                print(f"Inserted {i + 1} rows into StoreStatus")
        print(f"Loaded {StoreStatus.objects.count()} rows into StoreStatus")

    def parse_timestamp(self, timestamp_str, store_id):
        timestamp_str = timestamp_str.replace(" UTC", "")
        naive_datetime = self.parse_naive_datetime(timestamp_str)
        timezone_str = self.get_store_timezone(store_id)
        tz = pytz.timezone(timezone_str)
        return tz.localize(naive_datetime, is_dst=None)

    def parse_naive_datetime(self, timestamp_str):
        try:
            return datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            return datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')

    def get_store_timezone(self, store_id):
        default_timezone = 'America/Chicago'
        try:
            store_timezone = StoreTimezone.objects.get(store_id=store_id)
            return store_timezone.timezone_str
        except StoreTimezone.DoesNotExist:
            return default_timezone

    def load_business_hours(self):
        batch_size = 1000
        business_hours_entries = []
        with open('Menu hours.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for i, row in enumerate(reader):
                business_hours_entries.append(BusinessHours(
                    store_id=row[0],
                    day=row[1],
                    start_time_local=row[2],
                    end_time_local=row[3]
                ))
                
                if len(business_hours_entries) >= batch_size:
                    BusinessHours.objects.bulk_create(business_hours_entries)
                    print(f"Inserted {i + 1} rows into BusinessHours")
                    business_hours_entries = []

            if business_hours_entries:
                BusinessHours.objects.bulk_create(business_hours_entries)
                print(f"Inserted {i + 1} rows into BusinessHours")
        print(f"Loaded {BusinessHours.objects.count()} rows into BusinessHours")

    def load_store_timezone(self):
        batch_size = 1000
        store_timezone_entries = []
        with open('bq-results-20230125-202210-1674678181880.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for i, row in enumerate(reader):
                store_timezone_entries.append(StoreTimezone(
                    store_id=row[0],
                    timezone_str=row[1]
                ))
                
                if len(store_timezone_entries) >= batch_size:
                    StoreTimezone.objects.bulk_create(store_timezone_entries)
                    print(f"Inserted {i + 1} rows into StoreTimezone")
                    store_timezone_entries = []

            if store_timezone_entries:
                StoreTimezone.objects.bulk_create(store_timezone_entries)
                print(f"Inserted {i + 1} rows into StoreTimezone")
        print(f"Loaded {StoreTimezone.objects.count()} rows into StoreTimezone")
