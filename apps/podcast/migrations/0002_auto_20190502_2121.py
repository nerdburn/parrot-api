# Generated by Django 2.2 on 2019-05-02 21:21

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='podcast',
            name='last_synced_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 5, 2, 21, 21, 16, 688692, tzinfo=utc)),
        ),
    ]
