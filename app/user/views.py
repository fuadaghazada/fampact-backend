from django.http import Http404
from rest_framework.generics import (
    RetrieveUpdateAPIView,
    CreateAPIView
)

from .serializers import (
    FamilySerializer,
    AddFamilyMemberSerializer,
    AddChildMemberSerializer
)


class RetrieveFamilyApiView(RetrieveUpdateAPIView):
    """Retrieve family API View"""
    serializer_class = FamilySerializer

    def get_object(self):
        if self.request:
            return self.request.user.family

        raise Http404


class AddFamilyMemberApiView(CreateAPIView):
    """Add member API view"""
    serializer_class = AddFamilyMemberSerializer


class AddChildMemberApiView(CreateAPIView):
    """Add child API view"""
    serializer_class = AddChildMemberSerializer
