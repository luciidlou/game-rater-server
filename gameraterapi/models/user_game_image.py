from django.db import models
from django.contrib.auth.models import User


class UserGameImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    action_pic = models.ImageField(
        upload_to='actionimages', height_field=None,
        width_field=None, max_length=None, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
