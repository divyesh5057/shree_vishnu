# Generated by Django 4.2.1 on 2023-06-07 05:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0029_alter_project_db_emp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project_db',
            name='project_inventory',
        ),
        migrations.AddField(
            model_name='project_db',
            name='project_doc',
            field=models.FileField(blank=True, null=True, upload_to='project_doc/'),
        ),
        migrations.CreateModel(
            name='primary_inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('project_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Project_db', to='account.project_db')),
            ],
        ),
    ]
