# Generated by Django 5.1.3 on 2024-12-03 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendance',
            old_name='clock_out_tiem',
            new_name='clock_out_time',
        ),
    ]
