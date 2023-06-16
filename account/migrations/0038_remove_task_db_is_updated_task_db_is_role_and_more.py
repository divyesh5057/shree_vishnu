# Generated by Django 4.2.1 on 2023-06-12 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0037_task_db_is_poverty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task_db',
            name='is_updated',
        ),
        migrations.AddField(
            model_name='task_db',
            name='is_role',
            field=models.BooleanField(default=True, max_length=200),
        ),
        migrations.AddField(
            model_name='task_db',
            name='total_hours',
            field=models.IntegerField(default=0),
        ),
    ]
