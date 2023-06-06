# Generated by Django 4.2.1 on 2023-05-31 09:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0025_part_img_doc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_img_doc',
            name='project_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_img_docs', to='account.project_db'),
        ),
    ]