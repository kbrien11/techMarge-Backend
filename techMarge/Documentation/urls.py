from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r"tools", views.ToolViewSet, basename="Tool")


urlpatterns = [
    path("register", views.createUser),
    path("login", views.login),
    path("createTool", views.createTool),
    path("fetchAllTools", views.fetchAllTools),
    path("fetchOneTool", views.fetchOneTool),
    path("compareTools", views.compareTools),
    path("searchToolData", views.searchToolData),
    path("searchSingleTool", views.searchSingleTool),
    path("prompt_gpt", views.prompt_gpt),
    path("addToFavorites", views.addToFavorites),
    path("fetchAllFavorites", views.fetchAllFavorites),
    path("filterData", views.filterData),
] + router.urls
