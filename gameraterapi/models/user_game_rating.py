from django.db import models
from django.contrib.auth.models import User


class UserGameRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    datetime = models.DateTimeField()
