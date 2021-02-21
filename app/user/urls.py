from django.urls import path
from .views import (
    RetrieveFamilyApiView,
    AddFamilyMemberApiView,
    AddChildMemberApiView
)

app_name = 'user'

urlpatterns = [
    path(
        'family/',
        RetrieveFamilyApiView.as_view(),
        name="family"
    ),
    path(
        'add_member/',
        AddFamilyMemberApiView.as_view(),
        name="add_member"
    ),
    path(
        'add_child/',
        AddChildMemberApiView.as_view(),
        name="add_child"
    )
]
