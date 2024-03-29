# Generated by Django 4.1.5 on 2023-01-29 11:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0003_remove_submission_for_question_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="question",
            name="serial_num",
        ),
        migrations.AddField(
            model_name="offlinequestion",
            name="serial_num",
            field=models.SmallIntegerField(default=1, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="onlinequestion",
            name="serial_num",
            field=models.SmallIntegerField(default=1, unique=True),
            preserve_default=False,
        ),
    ]
