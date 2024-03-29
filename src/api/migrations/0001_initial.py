# Generated by Django 4.1.4 on 2023-01-01 17:20

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "contents",
                    ckeditor_uploader.fields.RichTextUploadingField(
                        blank=True, default=None, null=True
                    ),
                ),
                ("answer", models.CharField(max_length=100)),
                ("serial_num", models.SmallIntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="OfflineQuestion",
            fields=[
                (
                    "question_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="api.question",
                    ),
                ),
            ],
            bases=("api.question",),
        ),
        migrations.CreateModel(
            name="OnlineQuestion",
            fields=[
                (
                    "question_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="api.question",
                    ),
                ),
            ],
            bases=("api.question",),
        ),
        migrations.CreateModel(
            name="Submission",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text_contents", models.CharField(max_length=1024)),
                ("time_submitted", models.DateTimeField(auto_now_add=True)),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("ODT", "Outdated"),
                            ("COR", "Correct"),
                            ("INC", "Incorrect"),
                        ],
                        default=None,
                        editable=False,
                        max_length=3,
                    ),
                ),
                (
                    "by_player",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.player",
                    ),
                ),
                (
                    "for_question",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="api.question",
                    ),
                ),
            ],
        ),
    ]
