# Generated by Django 4.2.1 on 2023-06-08 05:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0031_rename_inventory_project_db_secondary_inventory_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer_db',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=20)),
                ('company_name', models.CharField(default='', max_length=100)),
                ('address', models.TextField()),
                ('customer_description', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Supplier_db',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplier_name', models.CharField(max_length=255)),
                ('supplier_email', models.EmailField(max_length=254, unique=True)),
                ('supplier_phone_number', models.CharField(max_length=20)),
                ('supplier_address', models.TextField()),
                ('supplier_description', models.TextField(default='')),
            ],
        ),
        migrations.AddField(
            model_name='primary_inventory',
            name='supplier_id',
            field=models.ManyToManyField(blank=True, default=None, null=True, to='account.supplier_db'),
        ),
        migrations.AddField(
            model_name='project_db',
            name='customer_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Project_db', to='account.customer_db'),
        ),
    ]
