# Generated by Django 4.1.7 on 2023-03-23 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_parts_db_working_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='parts_db',
            name='total_hours',
            field=models.CharField(default=False, max_length=200),
        ),
    ]