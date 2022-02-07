from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    designer = models.CharField(max_length=50)
    year_released = models.PositiveIntegerField()
    num_of_players = models.PositiveIntegerField()
    estimated_play_time = models.PositiveIntegerField()
    age_recommendation = models.PositiveIntegerField()
    categories = models.ManyToManyField("Category", through="gamecategory", related_name="categories")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
