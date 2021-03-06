# Generated by Django 2.2 on 2019-05-03 17:01

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(max_length=140, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Podcast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artwork_url', models.URLField()),
                ('feed_url', models.URLField()),
                ('link', models.URLField()),
                ('title', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField()),
                ('last_synced_date', models.DateTimeField(blank=True, default=datetime.datetime(2019, 5, 3, 17, 1, 37, 808426, tzinfo=utc))),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='podcast.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('content', models.TextField()),
                ('content_snippet', models.TextField()),
                ('published_date', models.DateTimeField()),
                ('link', models.URLField()),
                ('audio_url', models.URLField()),
                ('duration_seconds', models.IntegerField()),
                ('podcast', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='podcast.Podcast')),
            ],
        ),
    ]
