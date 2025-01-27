# Generated by Django 5.1 on 2024-08-27 12:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('monitor', '0006_delete_storebusinesshours_delete_storestatus_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('store_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('timezone_str', models.CharField(default='America/Chicago', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='StatusRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp_utc', models.DateTimeField()),
                ('status', models.CharField(max_length=10)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.store')),
            ],
        ),
        migrations.CreateModel(
            name='BusinessHour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField()),
                ('start_time_local', models.TimeField()),
                ('end_time_local', models.TimeField()),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.store')),
            ],
        ),
    ]
