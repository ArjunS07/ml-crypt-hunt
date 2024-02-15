from django.urls import path, re_path
from django.views.generic import TemplateView
from django.conf import settings

from utils.timing import get_crypthunt_status, EventStatus
from . import views

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path("login", views.Login.as_view(), name="login"),
    path("logout", views.Logout.as_view(), name="logout"),
    path("leaderboard", views.leaderboard, name="leaderboard"),
    path("about", TemplateView.as_view(template_name="about.html"), name="about"),
]

if not settings.IS_ONLINE_MODE and get_crypthunt_status() == EventStatus.OPEN:
    urlpatterns += [
        path("play", views.OfflinePlay.as_view(), name="play"),
    ]

if get_crypthunt_status() == EventStatus.OPEN:
    urlpatterns += [
        path("play", views.play, name="play"),
    ]

# Set up redirects for the play page if the Crypt Hunt is closed
elif get_crypthunt_status() == EventStatus.PAUSED:
    urlpatterns += [
        path("play", views.paused, name="play"),
    ]

elif get_crypthunt_status() == EventStatus.CLOSED:
    urlpatterns += [
        path("play", views.closed, name="play"),
    ]

elif get_crypthunt_status() == EventStatus.WAITING:
    # Before the event opens, we want to show the waiting page. As a fallback, also show it if the status is not properly configured
    urlpatterns += [
        path("play", views.waiting, name="play"),
    ]

if settings.DEBUG:
    urlpatterns += [
        # closed, waiting, and paused paths should be available at their paths in debug
        path("closed", views.closed, name="closed"),
        path("waiting", views.waiting, name="waiting"),
        path("paused", views.paused, name="paused"),
        path("congrats", views.congrats, name="congrats"),
    ]
