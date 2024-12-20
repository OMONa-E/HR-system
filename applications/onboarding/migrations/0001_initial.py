# Generated by Django 5.1.3 on 2024-12-02 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.CharField(max_length=15, unique=True)),
                ('employee_nin', models.CharField(max_length=25, unique=True)),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('job_title', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=15)),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('date_created', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
