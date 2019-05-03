# Generated by Django 2.2 on 2019-05-02 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('podcast', '0001_initial'),
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
            ],
        ),
    ]