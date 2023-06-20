"""djangoHeroku URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from .api.views import index_view, UserViewSet, GroupViewSet, EventViewSet, Interested_In_EventViewSet, PlaceViewSet, CommentViewSet
from .users.views import CustomRegisterView

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('groups', GroupViewSet)
router.register('events', EventViewSet)
router.register('interested', Interested_In_EventViewSet)
router.register('places', PlaceViewSet)
router.register('comments', CommentViewSet)

urlpatterns = [
    # http://localhost:8000/
    path('', index_view, name='index'),

    # http://localhost:8000/api/<router-viewsets>
    path('api/', include(router.urls)),

    path('api/explorer/', include('rest_framework.urls', namespace='rest_framework')),

    path('api/dj-rest-auth/', include('dj_rest_auth.urls')),
    path('api/dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),

    # http://localhost:8000/api/admin/
    path('api/admin/', admin.site.urls),

    path('api/register/', CustomRegisterView.as_view(), name='register'),
]
