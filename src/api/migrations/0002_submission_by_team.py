# Generated by Django 4.1.5 on 2023-01-10 18:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_team_current_question"),
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="submission",
            name="by_team",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="users.team",
            ),
        ),
    ]
