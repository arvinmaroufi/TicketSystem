# Generated by Django 5.2 on 2025-04-20 23:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticketmessage',
            name='is_internal',
        ),
    ]
