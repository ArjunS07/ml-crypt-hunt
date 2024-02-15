from django.urls import path, re_path

from . import views
from utils import timing

urlpatterns = [
    # This is the only path we're currently using
    path("submissions/", views.SubmissionsView.as_view(), name="submissions"),
    # path("login", views.LoginView.as_view(), name="login"),
    # path("question/", views.QuestionView.as_view(), name="question"),
    # path("teams/", views.TeamsView.as_view(), name="teams"),
    # path("players/", views.PlayersView.as_view(), name="players"),
    # path("levelup-team", views.LevelUpTeamView.as_view(), name="levelup-team"),
]

if timing.get_crypthunt_status() != timing.EventStatus.OPEN:
    urlpatterns.insert(
        0, re_path(r"^", views.CryptHuntClosedView.as_view(), name="closed")
    )
