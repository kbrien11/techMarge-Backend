from django.db import models
from django.contrib.auth.models import User


User._meta.get_field("email")._unique = True
User._meta.get_field("username")._unique = True


class Tool(models.Model):
    type = models.CharField(default="", max_length=40)
    location = models.CharField(default="", max_length=40)
    title = models.CharField(default="", max_length=40)
    description = models.CharField(default="")
    docLink = models.CharField(default="", max_length=100)
    language = models.CharField(default="", max_length=30)


class GitHubTools(models.Model):
    name = models.CharField(default="", blank=True, null=True)
    description = models.CharField(default="", blank=True, null=True)
    language = models.CharField(default="", blank=True, null=True)
    stargazers_count = models.IntegerField(default=0, blank=True, null=True)
    popularity = models.CharField(default="", blank=True, null=True)
    created_at = models.CharField(default="", blank=True, null=True)
    homepage = models.URLField(default="", blank=True, null=True)
