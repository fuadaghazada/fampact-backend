from django.urls import path
from .views import (
    LoginAPIView,
    VerifyAPIView,
    ForgotAPIView,
    SetPasswordAPIView,
    LogoutAPIView,
    RegisterAPIView
)

app_name = 'authentication'

urlpatterns = [
    path('token/', LoginAPIView.as_view(), name="login"),
    path('forgot/', ForgotAPIView.as_view(), name="forgot"),
    path('verify/<int:pk>/', VerifyAPIView.as_view(), name="verify"),
    path(
        'set_password/<int:pk>/<str:token>/',
        SetPasswordAPIView.as_view(),
        name="set_password"
    ),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('register/', RegisterAPIView.as_view(), name="register")
]
