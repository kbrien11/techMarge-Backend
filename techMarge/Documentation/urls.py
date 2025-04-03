from django.urls import path, include
from . import views

from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path("register", views.createUser),
    path("login", views.login),
    path("createTool", views.createTool),
    path("fetchAllTools", views.fetchAllTools),
    path("fetchOneTool", views.fetchOneTool),
    path("compareTools", views.compareTools),
]
