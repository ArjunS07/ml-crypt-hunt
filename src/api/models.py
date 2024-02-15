from django.utils.timezone import make_aware

from django.db import models

from ckeditor_uploader.fields import RichTextUploadingField

from users.models import Team, Player
from utils import functions


class Question(models.Model):
    """Class to represent a question. Subclass it as an online or offline question"""

    # Use CKEditor to allow for rich text editing. Will get rendered to HTML in the frontend template
    contents = RichTextUploadingField(default=None, blank=True, null=True)
    answer = models.CharField(max_length=100)

    # Override the save function to make sure the text is cleaned before saving
    def __save__(self, *args, **kwargs):
        self.answer = functions.clean_answer_text(self.answer)
        super().save(*args, **kwargs)

    @property
    def next_question(self):
        try:
            matching = self.__class__.objects.get(serial_num=self.serial_num + 1)
            return matching
        except self.__class__.DoesNotExist:
            return None


class OnlineQuestion(Question):
    """Wrapper class to represent online questions"""

    # Make the question editable to allow reordering
    serial_num = models.SmallIntegerField(unique=True)

    # Define fucntions for comparison operators to make queries easier
    def __lt__(self, other):
        return self.serial_num < other.serial_num

    def __gte__(self, other):
        return self.serial_num >= other.serial_num

    def __str__(self):
        return f"Online Question {self.serial_num} - {self.contents}"


class OfflineQuestion(Question):
    # Make the question editable to allow reordering
    serial_num = models.SmallIntegerField(unique=True)

    # Define fucntions for comparison operators to make queries easier
    def __lt__(self, other):
        return self.serial_num < other.serial_num

    def __gte__(self, other):
        return self.serial_num >= other.serial_num

    """Wrapper class to represent offline questions"""

    def __str__(self):
        return f"Offline Question {self.serial_num} - {self.contents}"


class Submission(models.Model):
    for_online_question = models.ForeignKey(
        OnlineQuestion, on_delete=models.SET_NULL, null=True, default=None, blank=True
    )
    for_offline_question = models.ForeignKey(
        OfflineQuestion, on_delete=models.SET_NULL, null=True, default=None, blank=True
    )

    @property
    def for_question(self):
        if self.for_online_question is not None:
            return self.for_online_question
        elif self.for_offline_question is not None:
            return self.for_offline_question
        else:
            raise ValueError("Submission has no question")

    text_contents = models.CharField(max_length=1024)

    time_submitted = models.DateTimeField(auto_now_add=True)
    by_player: Player = models.ForeignKey(
        Player, on_delete=models.CASCADE, default=None, null=True
    )
    by_team: Team = models.ForeignKey(
        Team, on_delete=models.CASCADE, default=None, null=True
    )

    STATUS_CHOICES = [("ODT", "Outdated"), ("COR", "Correct"), ("INC", "Incorrect")]
    status = models.CharField(
        max_length=3, choices=STATUS_CHOICES, default=None, blank=True, editable=False
    )

    def validate(self):
        if (
            self.for_online_question is not None
            and self.for_offline_question is not None
        ):
            raise ValueError(
                "Submission cannot have both online and offline questions associated with it"
            )

        # Check that people are not submitting for a question that is out of date
        if self.by_team.current_question != self.for_question:
            print(
                f'Outdated submission: "{self.text_contents}" by {self.by_player} for {self.for_question} (current question is {self.by_team.current_question}'
            )
            self.status = "ODT"
        # Clean the text contents to make it easier for teams. Questions must be stored with the cleaned version in the datbase.
        elif (
            # We use a cleaned version of the submission contents at comparison, rather than storing a cleaned version permanently, to allow for admins to view the exact submission as it was
            functions.clean_answer_text(self.text_contents)
            == functions.clean_answer_text(self.for_question.answer)
        ):
            print("Correct submission")
            self.status = "COR"
            self.by_team.advance_question()
        else:
            print("Incorrect submission")
            self.status = "INC"

    def save(self, *args, **kwargs):
        self.by_team = self.by_player.team
        self.validate()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.text_contents}"
