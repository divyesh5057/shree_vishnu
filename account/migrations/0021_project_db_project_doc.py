# Generated by Django 4.1.7 on 2023-05-29 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0020_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='project_db',
            name='project_doc',
            field=models.FileField(blank=True, null=True, upload_to='project_dox/'),
        ),
    ]