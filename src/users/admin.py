from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

admin.site.register(models.User, UserAdmin)

from django.contrib.sessions.models import Session
class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']
admin.site.register(Session, SessionAdmin)

@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "current_question_num",
        "total_points",
        "formatted_levelup_time",
    )

    def current_question_num(self, obj):
        if obj.current_question is None:
            return None
        return obj.current_question.serial_num

    current_question_num.order_field = "current_question__serial_num"
    current_question_num.short_description = "Current Question"
    ordering = ("-total_points", "levelup_time")


@admin.register(models.Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("school_user_id", "team", "is_banned")
    search_fields = ("school_user_id", "team__account__username")


@admin.register(models.IPAddress)
class IPAddressAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "for_player")
    ordering = ("for_player",)
    search_fields = ("for_player__school_user_id", "ip_address")

    def for_player(self, obj):
        return obj.for_player.school_user_id


@admin.register(models.PlayerLoginTime)
class PlayerLoginTimeAdmin(admin.ModelAdmin):
    list_display = ("for_player", "login_time")
    ordering = ("for_player",)
    search_fields = ("for_player__school_user_id", "login_time")

    def for_player(self, obj):
        return obj.for_player.school_user_id
