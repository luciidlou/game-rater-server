from django.db import models
from django.contrib.auth.models import User

from gameraterapi.models.user_game_rating import UserGameRating


class Game(models.Model):

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    designer = models.CharField(max_length=50)
    year_released = models.PositiveIntegerField()
    num_of_players = models.PositiveIntegerField()
    estimated_play_time = models.PositiveIntegerField()
    age_recommendation = models.PositiveIntegerField()
    categories = models.ManyToManyField(
        "Category", through="gamecategory", related_name="categories")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user')

    @property
    def uploaded(self):   # pylint: disable=missing-function-docstring
        return self.__uploaded

    @uploaded.setter
    def uploaded(self, value):
        self.__uploaded = value

    @property
    def average_rating(self):
        """Average rating calculated attribute for each game"""
        ratings = UserGameRating.objects.filter(game=self)
        total_rating = 0
        for rating in ratings:
            # Sum all of the ratings for the game
            total_rating += rating.rating
            # Calculate the average and return it.
            # If you don't know how to calculate average, Google it.
