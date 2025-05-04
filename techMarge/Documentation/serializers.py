from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from .models import CustomPaginator, Tool, GitHubTools, Favorite


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "is_active",
        ]
        extra_kwargs = {
            "password": {"required": False},
            "first_name": {"required": False},
            "last_name": {"required": False},
            "email": {"required": False},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = ["type", "title", "description", "location", "docLink", "language"]


class GitHubToolsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GitHubTools
        fields = [
            "name",
            "description",
            "language",
            "stargazers_count",
            "popularity",
            "created_at",
            "homepage",
            "owner",
            "type",
            "location",
        ]


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ["name", "user_pk"]


class PaginatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomPaginator
        fields = [
            "total_items",
            "total_pages",
            "current_page",
            "has_next",
            "has_previous",
        ]
