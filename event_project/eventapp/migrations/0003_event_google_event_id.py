# Generated by Django 5.0.2 on 2024-03-01 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventapp', '0002_alter_event_event_end_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='google_event_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
