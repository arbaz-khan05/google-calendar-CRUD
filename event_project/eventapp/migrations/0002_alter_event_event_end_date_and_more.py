# Generated by Django 5.0.2 on 2024-03-01 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_end_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_start_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='form_filling_date',
            field=models.DateTimeField(),
        ),
    ]