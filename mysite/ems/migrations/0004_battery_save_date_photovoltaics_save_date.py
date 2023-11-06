# Generated by Django 4.2.5 on 2023-10-11 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ems', '0003_battery_photovoltaics_ems_accumulate_energy'),
    ]

    operations = [
        migrations.AddField(
            model_name='battery',
            name='save_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='photovoltaics',
            name='save_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]