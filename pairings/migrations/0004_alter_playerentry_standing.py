# Generated by Django 5.2.1 on 2025-06-17 20:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pairings', '0003_playerentry_draws_playerentry_standing'),
        ('standings', '0004_standing_games_tied_standing_matches_tied'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerentry',
            name='standing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pairing_entries', to='standings.standing'),
        ),
    ]
