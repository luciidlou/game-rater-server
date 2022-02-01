from django.db import models
from django.contrib.auth.models import User


class UserGameImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    url = models.ImageField()
    datetime = models.DateTimeField()
