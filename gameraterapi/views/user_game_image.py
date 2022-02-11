import base64
import uuid
from django.forms import ValidationError
from django.http import HttpResponseServerError
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from gameraterapi.models import UserGameImage, Game


class PostImageSerializer(serializers.ModelSerializer):
    """JSON serializer for images"""
    class Meta:
        model = UserGameImage
        fields = ('game', 'action_pic')


class UserGameImageView(ViewSet):
    """Views for game images"""

    def create(self, request):
        """Handles POST requests for game images"""

        game = Game.objects.get(pk=request.data['game'])

        format, imgstr = request.data["action_pic"].split(';base64,')

        ext = format.split('/')[-1]
        image = ContentFile(base64.b64decode(imgstr),
                            name=f'{request.data["game"]}-{uuid.uuid4()}.{ext}')

        game_img_obj = UserGameImage.objects.create(
            user=request.auth.user,
            game=game,
            action_pic=image
        )
        serializer = PostImageSerializer(game_img_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

        # serializer = PostImageSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save(user=request.auth.user, action_pic=data)
        # return Response(serializer.data)
