# Generated by Django 5.1 on 2024-08-27 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('monitor', '0004_delete_storebusinesshours_delete_storestatus_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreBusinessHours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_id', models.CharField(max_length=20)),
                ('day_of_week', models.IntegerField()),
                ('start_time_local', models.TimeField()),
                ('end_time_local', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='StoreStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_id', models.CharField(max_length=20)),
                ('timestamp_utc', models.DateTimeField()),
                ('status', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='StoreTimezone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_id', models.CharField(max_length=20)),
                ('timezone_str', models.CharField(max_length=50)),
            ],
        ),
    ]