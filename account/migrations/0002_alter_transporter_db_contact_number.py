# Generated by Django 4.1.7 on 2023-03-22 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transporter_db',
            name='contact_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
