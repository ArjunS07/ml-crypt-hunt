from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.conf import settings

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import OnlineQuestion, OfflineQuestion, Submission
from users.models import Team, Player

from rest_framework import serializers

from .models import Submission
from users.models import Player


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = [
            "text_contents",
            "time_submitted",
            "by_player",
            "by_team",
            "status",
        ]
        read_only_fields = fields


DEFAULT_SUBMISSIONS_COUNT_LIMIT = 100


class SubmissionsView(APIView):
    """GET team submissions, and POST a submission for your team"""

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        The only entry point for this application. Submitting an answer automatically triggers a levelup if it is correct.
        The view returns the status of the submission.
        Frontend clients can refresh the question if the submission is correct.
        """
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        account = request.user
        matching_team = get_object_or_404(Team, account=account)

        if matching_team.has_completed:
            return Response(
                "Your team has completed the hunt!",
                status=status.HTTP_403_FORBIDDEN,
            )
        elif matching_team.is_banned:
            return Response(
                "Your team has been banned from the hunt.",
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            loggedin_player = Player.objects.get(id=request.session["player_id"])
        except Exception as e:
            return Response("Player not logged in", status=status.HTTP_401_UNAUTHORIZED)

        data = request.POST
        school_user_id = data.get("school_user_id", None)
        text_contents = data.get("contents", None)
        question_num = data.get("question_num", None)

        if not school_user_id or not text_contents or not question_num:
            print(f"{data=} {school_user_id=} {text_contents=}")
            return Response("Missing parameter", status=status.HTTP_400_BAD_REQUEST)

        if school_user_id != loggedin_player.school_user_id:
            return Response(
                "You are not logged in as the player you are submitting for",
                status=status.HTTP_401_UNAUTHORIZED,
            )

        matching_player = Player.objects.get_or_create(
            team=matching_team, school_user_id=school_user_id
        )[0]

        if settings.IS_ONLINE_MODE:
            for_question = get_object_or_404(OnlineQuestion, serial_num=question_num)
        else:
            for_question = get_object_or_404(OfflineQuestion, serial_num=question_num)

        try:
            new_submission = Submission(
                text_contents=text_contents,
                by_player=matching_player,
            )
            if settings.IS_ONLINE_MODE:
                new_submission.for_online_question = for_question
            else:
                new_submission.for_offline_question = for_question
            new_submission.save()
        except Exception as e:
            print(f"Error creating submission: {e=} {type(matching_player)}")
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Return the submission status
        return Response(
            SubmissionSerializer(new_submission).data, status=status.HTTP_201_CREATED
        )

class CryptHuntClosedView(APIView):
    """Use this view if the Crypt Hunt is closed."""

    def get(self, request):
        return Response({"is_closed": True}, status=status.HTTP_400_BAD_REQUEST)