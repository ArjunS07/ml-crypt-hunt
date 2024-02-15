# Generated by Django 4.1.5 on 2023-01-25 16:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_team_current_question"),
    ]

    operations = [
        migrations.AddField(
            model_name="team",
            name="color",
            field=models.CharField(
                blank=True,
                choices=[
                    ("red", "Red"),
                    ("green", "Green"),
                    ("blue", "Blue"),
                    ("yellow", "Yellow"),
                ],
                default=None,
                max_length=10,
                null=True,
            ),
        ),
    ]