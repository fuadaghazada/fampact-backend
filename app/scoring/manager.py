from django.db.models import Manager, Sum
from django.db.models.functions import Coalesce

from user.models import Family, User


class ScoreManager(Manager):
    """Score manager"""

    def public_leader_board_qs(self):
        return Family.objects \
            .annotate(
                score=Coalesce(Sum('family_members__user_scores__score'), 0)) \
            .order_by('-score')

    def private_leader_board_qs(self, family):
        return User.objects \
            .filter(family=family) \
            .annotate(score=Coalesce(Sum('user_scores__score'), 0)) \
            .order_by('-score')

    @classmethod
    def calculate_user_score(cls, user):
        return user.user_scores \
            .aggregate(score=Coalesce(Sum('score'), 0)) \
            .get('score')
