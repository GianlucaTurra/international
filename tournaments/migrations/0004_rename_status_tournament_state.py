# Generated by Django 5.2.1 on 2025-06-09 20:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0003_remove_tournament_completed_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tournament',
            old_name='status',
            new_name='state',
        ),
    ]
