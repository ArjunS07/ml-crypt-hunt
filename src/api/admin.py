from django.contrib import admin

from . import models


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("serial_num", "contents", "answer")
    ordering = ("serial_num",)


admin.site.register(models.OnlineQuestion, QuestionAdmin)
admin.site.register(models.OfflineQuestion, QuestionAdmin)


class SubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "status",
        "for_question",
        "text_contents",
        "by_player",
        "by_team",
        "time_submitted",
    )
    search_fields = (
        "text_contents",
        "by_player__school_user_id",
        "by_team__account__username",
    )
    ordering = ("-time_submitted",)

    def for_question(self, obj):
        return obj.for_question.serial_num

    for_question.order_field = "for_question__serial_num"
    for_question.short_description = "Question"


admin.site.register(models.Submission, SubmissionAdmin)
