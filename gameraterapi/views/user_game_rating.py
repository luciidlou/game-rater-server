from django.forms import ValidationError
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from gameraterapi.models import Game, Category, UserGameRating
from django.contrib.auth.models import User


class UserGameRatingView(ViewSet):
    """Views for user game ratings"""

    def list(self, request):
        """Executes a GET request to the server to get all games"""
        ratings = UserGameRating.objects.all()

        for rating in ratings:
            rating.is_rater = rating.user == request.auth.user

        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Executes a GET request to the server to get a single game"""
        rating = UserGameRating.objects.get(pk=pk)
        serializer = RatingSerializer(rating)
        return Response(serializer.data)

    def create(self, request):
        """Executes a POST request to the server to create a game"""
        game = Game.objects.get(pk=request.data['game'])
        user = User.objects.get(pk=request.auth.user_id)
        serializer = CreateRatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(game=game, user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Executes a PUT request to the server to update a specific single game"""
        rating = UserGameRating.objects.get(pk=pk)

        rating.rating = request.data['rating']

        rating.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Performs a DELETE request on the specified game"""
        rating = UserGameRating.objects.get(pk=pk)
        rating.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class RatingSerializer(serializers.ModelSerializer):
    """JSON serializer for game ratings"""
    class Meta:
        model = UserGameRating
        fields = ('id', 'user', 'game', 'rating', 'datetime', 'is_rater')
        depth = 1


class CreateRatingSerializer(serializers.ModelSerializer):
    """JSON serializer for game ratings"""
    class Meta:
        model = UserGameRating
        fields = ('game', 'rating')
