# Generated by Django 4.2.1 on 2023-05-05 13:11

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0005_alter_team_levelup_time"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="ipaddress",
            options={"verbose_name_plural": "IP Addresses"},
        ),
    ]
