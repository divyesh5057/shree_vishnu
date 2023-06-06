# Generated by Django 4.2.1 on 2023-05-31 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0023_userupdate_db_end_time_userupdate_db_start_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project_db',
            name='project_doc',
        ),
        migrations.CreateModel(
            name='Project_img_doc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_doc', models.FileField(blank=True, null=True, upload_to='project_doc/')),
                ('project_img', models.ImageField(blank=True, null=True, upload_to='project_img/')),
                ('project_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.project_db')),
            ],
        ),
    ]
