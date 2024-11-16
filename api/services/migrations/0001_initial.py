# Generated by Django 5.1.3 on 2024-11-16 15:19

import django.db.models.deletion
import timescale.db.models.fields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(blank=True, choices=[('type1', 'TYPE1'), ('type2', 'TYPE2')], max_length=100, null=True)),
                ('status', models.CharField(choices=[('active', 'ACTIVE'), ('inactive', 'INACTIVE')], default='inactive', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=10)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=10)),
                ('altitude', models.DecimalField(decimal_places=2, max_digits=10)),
                ('speed', models.DecimalField(decimal_places=2, max_digits=10)),
                ('time', timescale.db.models.fields.TimescaleDateTimeField(interval='1 day')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='services.device')),
            ],
        ),
    ]
