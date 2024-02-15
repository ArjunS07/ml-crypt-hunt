import random
import csv
import string
import re
import datetime
import requests

from users import models as user_models
from api import models
from . import constants

"""Application functions"""

def get_ip_address_from_request(request) -> str:
    """
    Get the IP address of the user from the request object
    """
    return request.META.get(
        "HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR", None)
    )


def clean_answer_text(text: str) -> str:
    return (
        text.strip()
        .lower()
        .replace(" ", "")
        .translate(str.maketrans("", "", string.punctuation))
    )


def clean_school_user_id(id: str) -> str: 
    return id.strip().lower().replace(" ", "").replace("@", "").replace("internal.tsrs.org", "").replace("tsrs.org", "")

def is_school_id_valid(school_id: str) -> str:
    print(f"Checking if school id  {school_id} is valid")
    # print the matching id in constants.VALID_USERNAMES_LIST
    for valid_id in constants.VALID_USERNAMES_LIST:
        if school_id == clean_school_user_id(valid_id):
            print(f"School id {school_id} is valid, matched with {valid_id}")
            return True
    print(f"School id {school_id} is invalid")


"""Admin side convenience utilities"""
def _generate_passphrase(length: int) -> str:
    passphrase = ""
    for i in range(length):
        passphrase += f"{random.choice(constants.WORD_LIST)}"
        if i != length - 1:
            passphrase += "-"
    return passphrase


def generate_teams(
    team_names: list[str] = constants.HOUSE_NAMES,
    team_colors: list[str] = constants.HOUSE_COLORS,
    password_length: int = 3,
) -> list[user_models.Team]:
    print(
        "Generating passwords using clean_words.txt and printing whatsapp message from constants.py"
    )

    for house_name, house_color in zip(team_names, team_colors):
        passphrase = _generate_passphrase(length=password_length)
        user = user_models.User(username=house_name)
        user.set_password(passphrase)
        user.save()

        team = user_models.Team(account=user, color=house_color)

        if models.OnlineQuestion.objects.count() > 0:
            team.current_online_question = models.OnlineQuestion.objects.get(
                serial_num=1
            )
        if models.OfflineQuestion.objects.count() > 0:
            team.current_offline_question = models.OfflineQuestion.objects.get(
                serial_num=1
            )
        team.save()

        message = (
            constants.WHATSAPP_MESSAGES["share_password_message"]
            .replace("{{HOUSE_NAME}}", house_name)
            .replace("{{HOUSE_PASSWORD}}", passphrase)
        )
        print(message)


def reset_teams_levels(teams=models.Team.objects.all()):
    for team in teams:
        team.current_online_question = models.OnlineQuestion.objects.get(serial_num=1)
        team.current_offline_question = models.OfflineQuestion.objects.get(serial_num=1)
        team.total_points = 0
        team.save()
        print(f"Successfully reset {team.account.username}")


def export_team_submissions(team: models.Team) -> str:
    """Saves all submissions for a team to a CSV file and returns a `file.io` link to download it from Heroku"""
    submissions: list[models.Submission] = models.Submission.objects.filter(
        by_team=team
    )
    if len(submissions) == 0:
        print(f"No submissions found for {team.account.username} ")
        return None
    # Create a CSV file
    now: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    path: str = (
        f"{constants.BASE_DIR}/{team.account.username}_submissions__{now}.csv".replace(
            " ", "_"
        )
    )
    with open(path, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Time", "By", "Question", "Submission", "Status"])
        for submission in submissions:
            writer.writerow(
                [
                    submission.time_submitted.strftime("%Y-%m-%d %H:%M:%S"),
                    submission.by_player.school_user_id,
                    submission.for_question.serial_num,
                    submission.text_contents,
                    submission.status,
                ]
            )
    # Upload the file to file.io
    with open(path, "rb") as f:
        res = requests.post("https://file.io", files={"file": f})
        print(res.json())
        return res.json()["link"]

def export_players_csv(team: models.Team) -> str:
    """Saves all players of a team to a CSV and returns a `file.io` link to download it from Heroku"""
    players = user_models.Player.objects.filter(team=team)
    if len(players) == 0:
        print(f"No players found for {team.account.username} ")
        return None
    # Create a CSV file
    now: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    path: str = (
        f"{constants.BASE_DIR}/{team.account.username}_players__{now}.csv".replace( " ", "_")
    )
    with open(path, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["School User ID", "First logged IP", "Last Logged IP", "First login time", "Last login time"])
        for player in players:
            row = [player.school_user_id, None, None, None, None]
            if len(player.logged_ips) > 0:
                row[1] = list(player.logged_ips)[0].ip_address
                if len(player.logged_ips) > 1:
                    row[2] = list(player.logged_ips)[-1].ip_address
            if len(player.login_times) > 0:
                row[3] = list(player.login_times)[0].login_time.strftime("%Y-%m-%d %H:%M:%S")
                if len(player.login_times) > 1:
                    row[4] = list(player.login_times)[-1].login_time.strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow(row)
    
    with open(path, "rb") as f:
        res = requests.post("https://file.io", files={"file": f})
        print(res.json())
        return res.json()["link"]
    
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

def export_sessions():
    session_objects = Session.objects.all()
    with open("session-dump.csv", "w") as f:
        writer = csv.writer(f)
        for session_object in session_objects:
            row = [session_object.session_key, session_object.session_data, session_object.expire_date]
            writer.writerow(row)
    with open("session-dump.csv", "rb") as f:
        res = requests.post("https://file.io", files={"file": f})
        print(res.json())
        return res.json()["link"]