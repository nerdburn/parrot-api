# Generated by Django 2.2 on 2019-05-03 17:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('podcast', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Moment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_second', models.PositiveIntegerField()),
                ('end_second', models.PositiveIntegerField()),
                ('short_code', models.SlugField()),
                ('created_at', models.DateTimeField()),
                ('rehypes_count', models.PositiveIntegerField()),
                ('listen_count', models.PositiveIntegerField()),
                ('like_count', models.PositiveIntegerField()),
                ('episode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='podcast.Episode')),
                ('podcast', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='podcast.Podcast')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
