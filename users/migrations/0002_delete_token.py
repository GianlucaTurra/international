# Generated by Django 5.2.1 on 2025-06-09 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Token',
        ),
    ]
