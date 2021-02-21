from django.urls import path
from .views import (
    PublicLeaderBoardAPIView,
    FamilyMemberLeaderBoardAPIView
)

app_name = 'scoring'

urlpatterns = [
    path(
        'public_leader_board/',
        PublicLeaderBoardAPIView.as_view(),
        name="public_lb"
    ),
    path(
        'private_leader_board/',
        FamilyMemberLeaderBoardAPIView.as_view(),
        name="private_lb"
    )
]
