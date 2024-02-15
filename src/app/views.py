from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout

from api.models import OfflineQuestion, OnlineQuestion
from users.models import Team, Player, IPAddress, PlayerLoginTime
from utils.functions import (
    get_ip_address_from_request,
    is_school_id_valid,
    clean_school_user_id,
)

class Login(View):
    def get(self, request):
        # Check if the user is an admin
        if request.user.is_superuser:
            return redirect("admin:index")

        if request.user.is_authenticated:
            return redirect("play")

        teams = Team.objects.all().order_by("account__username")
        return render(request, "login.html", context={"teams": teams})

    def post(self, request):
        teams = Team.objects.all().order_by("account__username")

        if request.user.is_authenticated:
            return redirect("play")

        team_username = request.POST.get("team-username", None)
        password = request.POST.get("team-password", None)
        player_id = request.POST.get("player-id", None)

        if team_username is None or password is None or player_id is None:
            return render(
                request,
                "login.html",
                context={"error": "Please fill all the fields.", "teams": teams},
            )
        account = authenticate(username=team_username, password=password)
        if account is None:
            return render(
                request,
                "login.html",
                context={
                    "error": "Invalid house password. Please check your house WhatsApp group for the correct password.",
                    "teams": teams,
                },
            )

        team = get_object_or_404(Team, account=account)

        player_id = clean_school_user_id(player_id)
        try:
            player = Player.objects.get(team=team, school_user_id=player_id)
        except:
            if not is_school_id_valid(player_id):
                print(f"Invalid school ID {player_id=}")
                return render(
                    request,
                    "login.html",
                    context={
                        "error": "Your school ID is not valid. Please contact the OC if you think this is a mistake.",
                        "teams": teams,
                    },
                )
            try:
                player = Player(team=team, school_user_id=player_id)
                player.full_clean()
                player.save()
            except:
                print(f"Taken school ID {player_id=}")
                return render(
                    request,
                    "login.html",
                    context={
                        "error": "Your school ID is already taken by a user from another house. Please contact the OC if you think this is a mistake.",
                        "teams": teams,
                    },
                )

        request_ip = get_ip_address_from_request(request)
        if not IPAddress.objects.filter(ip_address=request_ip).exists():
            ip_address = IPAddress(ip_address=request_ip, for_player=player)
            ip_address.save()

        player_login_time = PlayerLoginTime(for_player=player)
        player_login_time.save()

        request.session["player_id"] = player.id
        login(request, account)
        return redirect("play")


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect("index")


def play(request):
    if not request.user.is_authenticated:
        return redirect("login")

    account = request.user
    team = get_object_or_404(Team, account=account)

    if team.has_completed:
        return render(request, "congrats.html")

    try:
        loggedin_player = Player.objects.get(id=request.session["player_id"])
    except:
        logout(request)
        return redirect("login")

    question = team.current_question

    if request.method == "GET":
        if team.is_banned:
            return render(request, "team-banned.html")
        if loggedin_player.is_banned:
            return render(request, "player-banned.html")
        return render(
            request,
            "play.html",
            context={"question": question, "player": loggedin_player},
        )


def leaderboard(request):
    teams = Team.objects.all().order_by(
        "-total_points", "levelup_time", "account__username"
    )
    any_team_on_0_points = any([team.total_points == 0 for team in teams])
    return render(
        request,
        "leaderboard.html",
        context={"teams": teams, "any_on_0": any_team_on_0_points},
    )


# Views which replace the play page if the Crypt Hunt is closed. Refer to urls.py for more info
def waiting(request):
    return render(request, "waiting.html")


def paused(request):
    return render(request, "paused.html")


def closed(request):
    return render(request, "closed.html")


def congrats(request):
    return render(request, "congrats.html")



class OfflinePlay(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("login")

        account = request.user
        team = get_object_or_404(Team, account=account)

        offline_questions = OfflineQuestion.objects.all()

        try:
            loggedin_player = Player.objects.get(id=request.session["player_id"])
        except:
            logout(request)
            return redirect("login")

        if request.method == "GET":
            if team.is_banned:
                return render(request, "team-banned.html")
            if loggedin_player.is_banned:
                return render(request, "player-banned.html")
            return render(
                request,
                "offline.html",
                context={"questions": offline_questions, "player": loggedin_player},
            )
