# Generated by Django 4.2.20 on 2025-03-19 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read_records', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='designation',
            field=models.CharField(default='', max_length=100),
        ),
    ]
