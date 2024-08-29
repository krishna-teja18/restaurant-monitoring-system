from django.db import models

class StoreStatus(models.Model):
    store_id = models.CharField(max_length=50)
    status = models.CharField(max_length=10)
    timestamp_utc = models.DateTimeField()

    def __str__(self):
        return f"{self.store_id} - {self.status} - {self.timestamp_utc}"

class BusinessHours(models.Model):
    store_id = models.CharField(max_length=50)
    day = models.IntegerField()
    start_time_local = models.TimeField()
    end_time_local = models.TimeField()

    def __str__(self):
        return f"{self.store_id} - {self.day}"

class StoreTimezone(models.Model):
    store_id = models.CharField(max_length=50)
    timezone_str = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.store_id} - {self.timezone_str}"

class Report(models.Model):
    report_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, default="Running")
    csv_file = models.FileField(upload_to='reports/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.report_id} - {self.status}"
