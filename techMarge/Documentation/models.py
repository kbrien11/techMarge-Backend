from django.db import models
from django.contrib.auth.models import User


User._meta.get_field("email")._unique = True
User._meta.get_field("username")._unique = True


class Tool(models.Model):
    type = models.CharField(default="", max_length=40)
    location = models.CharField(default="", max_length=40)
    title = models.CharField(default="", max_length=40)
    description = models.CharField(default="", max_length=30)
    docLink = models.CharField(default="", max_length=100)
    language = models.CharField(default="", max_length=30)
