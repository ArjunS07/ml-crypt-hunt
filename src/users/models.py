import re
from datetime import datetime

from django.utils.timezone import localtime, make_aware
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError

from utils import constants, timing


# Use a custom user model as a best practice in case we need to customise it later
class User(AbstractUser):
    pass


class Team(models.Model):

    """
    We use the same user model as the default Django user model to handle
    authentication for the entire team. This allows us to have one password
    and a shared object for all players in a team.
    """

    account = models.ForeignKey(User, on_delete=models.CASCADE)
    # Use a string ForeignKey to avoid circular imports
    current_online_question = models.ForeignKey(
        "api.OnlineQuestion", on_delete=models.SET_NULL, null=True, blank=True
    )
    current_offline_question = models.ForeignKey(
        "api.OfflineQuestion", on_delete=models.SET_NULL, null=True, blank=True
    )

    @property
    def current_question(self):
        if settings.IS_ONLINE_MODE == True:
            return self.current_online_question
        return self.current_offline_question

    # Store the last levelup time. This is used to calculate the order of the leaderboard
    levelup_time = models.DateTimeField(null=True, blank=True, default=None)
    is_banned = models.BooleanField(default=False)

    COLOR_CHOICES = [
        ("red", "Red"),
        ("green", "Green"),
        ("blue", "Blue"),
        ("yellow", "Yellow"),
    ]

    color = models.CharField(
        max_length=10, choices=COLOR_CHOICES, default=None, null=True, blank=True
    )

    @property
    def username(self):
        return self.account.username

    total_points = models.IntegerField(default=0)

    def __str__(self):
        if self.is_banned:
            return f"{self.account.username} (Banned)"
        return f"{self.account.username}"

    @property
    def formatted_levelup_time(self):
        if self.levelup_time:
            # Format the date and time as a string in the desired format: 12:00 PM, Monday for the leaderboard and admin panel
            formatted_date = localtime(self.levelup_time).strftime("%H:%M %p on %A")
            return formatted_date
        return None

    @property
    def has_completed(self):
        return (
            self.current_question is None
            and not self.is_banned
            and timing.is_crypthunt_open()
        )

    def advance_question(self):
        if settings.IS_ONLINE_MODE == True:
            try:
                self.current_online_question = self.current_question.next_question
                self.total_points += constants.ONLINE_POINTS_PER_QUESTION
            except AttributeError:
                self.current_online_question = None
        else:
            try:
                self.current_offline_question = self.current_question.next_question
                self.total_points += constants.OFFLINE_POINTS_PER_QUESTION
            except AttributeError:
                self.current_offline_question = None

        now = datetime.now()
        aware_datetime = make_aware(now)
        self.levelup_time = aware_datetime
        self.save()


# DO NOT delete this function, even though it is unused. Everything breaks if you delete it.
def school_user_id_validator(value: str) -> str:
    print(f"Validating username pattern {value}")
    if re.match(r"^[a-z]+\.[a-z]+[0-9]+$", value.lower().strip()):
        return value
    else:
        raise ValidationError("The school ID must be in the format john.doe1234")


class Player(models.Model):
    """
    We use this to represent a player in the database for internal tracking and logging purposes.

    We identify players with their school ID as a string.
    There are some obvious problems with this:
    - People can easily impersonate other people in the database by using their school ID
    - If banned, a player can easily create a new account with a false school ID and continue playing

    """

    school_user_id = models.CharField(max_length=100, unique=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    is_banned = models.BooleanField(default=False)

    @property
    def display_name(self):
        return f"{self.user_id} ({self.team})"

    @property
    def logged_ips(self):
        return IPAddress.objects.filter(for_player=self)

    @property
    def login_times(self):
        return PlayerLoginTime.objects.filter(for_player=self)

    def __str__(self) -> str:
        return f"{self.school_user_id}"

    def save(self, *args, **kwargs):
        self.school_user_id = self.school_user_id.strip().lower()
        super().save(*args, **kwargs)


class IPAddress(models.Model):
    ip_address = models.CharField(max_length=100)
    for_player = models.ForeignKey(Player, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.ip_address}"

    class Meta:
        verbose_name_plural = "IP Addresses"


class PlayerLoginTime(models.Model):
    for_player = models.ForeignKey(Player, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.login_time}"
