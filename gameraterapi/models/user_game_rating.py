from django.db import models
from django.contrib.auth.models import User


class UserGameRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    rating = models.FloatField()
    datetime = models.DateTimeField(auto_now_add=True)

    @property
    def is_rater(self):  # pylint: disable=missing-function-docstring
        return self.__is_rater

    @is_rater.setter
    def is_rater(self, value):
        self.__is_rater = value
