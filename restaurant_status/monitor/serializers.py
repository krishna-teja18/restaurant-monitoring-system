from rest_framework import serializers
from monitor.models import Report

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['report_id', 'status', 'csv_file']
