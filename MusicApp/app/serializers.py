from .models import Tracks, Genres
from rest_framework import serializers


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('id', 'name')


class GetTrackSerializer(serializers.ModelSerializer):
    # genre=GenreSerializer(source='genres_set',many=True)
    class Meta:
        model = Tracks
        fields = ('id', 'title', 'rating', 'genres')
        depth = 1




class TrackSerializer(serializers.ModelSerializer):


    # genre=GenreSerializer(source='genres_set',many=True)
    class Meta:
        model = Tracks
        fields = ('id', 'title', 'rating', 'genres')









