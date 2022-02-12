from django.contrib.auth.models import User
# from django.forms import ValidationError
# from django.http import HttpResponseServerError
from django.db.models import Q
from rest_framework import serializers, status
# from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from gameraterapi.models import Category, Game

# STEPS TO 'GET' WITH REST FRAMEWORK:
# 1. Use either the .get() or .all() ORM method. **.get() needs pk as arg**
# 2. Use serializer and pass in the object(s) as 1st argument **use 'many=True' as 2nd arg if listing**.
# 3. return Response(serializer.data)

# STEPS TO 'POST' WITH REST FRAMEWORK:
# 1. try: passing in the request.data dictionary as the data to the serializer. **serializer = CreateGameSerializer(data=request.data)**
# 2. Call 'is_valid' on the serializer to check if valid data was sent. **serializer.is_valid(raise_exception=True)**
# **Keys on the dictionary must match what is in the fields on the serializer**
# 3. use .save() on serializer to save the object.
# 4. return the data from the serializer in the Response and set a 204 status code.
# 5. execpt ValidationError as ex:
#    return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

# STEPS TO 'PUT' WITH REST FRAMEWORK:
# 1. Use .get() ORM method to get the object we are updating.
# 2. Using request.data['key'], update all the fields on the class instance.
# 3. Use the .save() method on the game we just updated.
# 4. return an empty Response with a 204 status code **Response(None, status=status.HTTP_204_NO_CONTENT)**

# STEPS TO 'DELETE' WITH REST FRAMEWORK:
# 1. Use .get() ORM method to get the object we are deleting (passing in pk).
# 2. Use .delete() method on the object.
# 3. return an empty Response with a 204 status code **Response(None, status=status.HTTP_204_NO_CONTENT)**


class GameView(ViewSet):
    def list(self, request):
        """Executes a GET request to the server to get all games"""
        search_text = self.request.query_params.get('q', None)
        filter_games = self.request.query_params.get('orderby', None)

        if search_text and filter_games:
            [param, order] = filter_games.split("/")
            if order == "desc":
                games = Game.objects.filter(
                    Q(title__contains=search_text) |
                    Q(description__contains=search_text) |
                    Q(designer__contains=search_text)
                ).order_by(f'-{param}')
            else:
                games = Game.objects.filter(
                    Q(title__contains=search_text) |
                    Q(description__contains=search_text) |
                    Q(designer__contains=search_text)
                ).order_by(f'{param}')

        elif search_text is not None:
            games = Game.objects.filter(
                Q(title__contains=search_text) |
                Q(description__contains=search_text) |
                Q(designer__contains=search_text)
            )

        elif filter_games is not None:
            [param, order] = filter_games.split("/")

            if order == "desc":
                games = Game.objects.order_by(f'-{param}')
            else:
                games = Game.objects.order_by(f'{param}')

        else:
            games = Game.objects.all()

        for game in games:
            game.uploaded = request.auth.user == game.user

        serializer = GameSerializer(games, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Executes a GET request to the server to get a single game"""
        game = Game.objects.get(pk=pk)
        game.uploaded = request.auth.user == game.user

        serializer = GameSerializer(game)

        return Response(serializer.data)

    def create(self, request):
        """Executes a POST request to the server to create a game"""
        category = Category.objects.get(pk=request.data['category'])
        user = User.objects.get(pk=request.auth.user_id)

        serializer = CreateGameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        game = serializer.save(user=user)
        game.categories.add(category)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

        # category = Category.objects.get(pk=request.data['category'])

        # game = Game.objects.create(
        #     title=request.data['title'],
        #     description=request.data['description'],
        #     designer=request.data['designer'],
        #     year_released=request.data['year_released'],
        #     num_of_players=request.data['num_of_players'],
        #     estimated_play_time=request.data['estimated_play_time'],
        #     age_recommendation=request.data['age_recommendation']
        # )
        # game.categories.add(category)
        # serializer = CreateGameSerializer(game)
        # return Response(serializer.data)

    def update(self, request, pk):
        """Executes a PUT request to the server to update a specific single game"""
        game = Game.objects.get(pk=pk)

        game.title = request.data['title']
        game.description = request.data['description']
        game.designer = request.data['designer']
        game.year_released = request.data['year_released']
        game.num_of_players = request.data['num_of_players']
        game.estimated_play_time = request.data['estimated_play_time']
        game.age_recommendation = request.data['age_recommendation']

        game.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Performs a DELETE request on the specified game"""
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""
    class Meta:
        model = Game
        fields = ('id', 'title', 'description', 'designer', 'year_released',
                  'num_of_players', 'estimated_play_time',
                  'age_recommendation', 'categories', 'user',
                  'uploaded', 'average_rating')
        depth = 2


# This serializer will include the fields that are expected from the client.
# Notice it does not have the gamer in the fields. Since the gamer comes from
# the Auth header it will not be in the request body

# ? The new serializer will be used to validate and save the new game in the create method
class CreateGameSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""
    class Meta:
        model = Game
        fields = ('id', 'title', 'description',
                  'designer', 'year_released', 'num_of_players',
                  'estimated_play_time', 'age_recommendation',
                  'categories')
