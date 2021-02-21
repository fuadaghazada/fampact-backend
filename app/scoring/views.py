from rest_framework.generics import ListAPIView

from .models import Score
from .serializers import (
    PublicLeaderBoardSerializer,
    FamilyMemberLeaderBoardSerializer
)


class PublicLeaderBoardAPIView(ListAPIView):
    """Leader board API view (public)"""
    queryset = Score.objects.public_leader_board_qs()
    serializer_class = PublicLeaderBoardSerializer


class FamilyMemberLeaderBoardAPIView(ListAPIView):
    """Leader board API view (family)"""
    queryset = Score.objects.public_leader_board_qs()
    serializer_class = FamilyMemberLeaderBoardSerializer

    def get_queryset(self):
        if self.request:
            return Score.objects.private_leader_board_qs(
                family=self.request.user.family
            )

        return self.queryset.none()
