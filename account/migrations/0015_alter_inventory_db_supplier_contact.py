# Generated by Django 4.1.7 on 2023-05-22 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_alter_parts_db_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory_db',
            name='supplier_contact',
            field=models.IntegerField(blank=True, max_length=11, null=True),
        ),
    ]