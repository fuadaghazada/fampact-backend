"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import AllowAny

API_PREFIX = 'api/v1'

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Docs
    path(f'{API_PREFIX}/docs/',
         include_docs_urls(title=settings.API_TITLE,
                           description=settings.API_DESCRIPTION,
                           permission_classes=[AllowAny])),

    # Authentication
    path(
        f'{API_PREFIX}/auth/',
        include('authentication.urls'),
        name='authentication'
    ),

    # Task
    path(
        f'{API_PREFIX}/task/',
        include('task.urls'),
        name='task'
    ),

    # Scoring
    path(
        f'{API_PREFIX}/scoring/',
        include('scoring.urls'),
        name='scoring'
    )
]

# Media links
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
