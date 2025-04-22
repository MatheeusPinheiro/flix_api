from rest_framework import serializers
from .models import Movie
from actors.serealizers import ActorSerializer
from genres.serializers import GenreSerializer
from django.db.models import Avg


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'
    
    def validate_release_date(self, value):
        if value < 1900:
            raise serializers.ValidationError('Somente filmes aparti de 1990 podem ser cadastrado.')
        return value
    
    def validate_resume(self, value):
        if value > 500:
            raise serializers.ValidationError('A resume do filme deve ter até 500 caracteres.')
        return value


class MovieListDetailSerializer(serializers.ModelSerializer):
    actors = ActorSerializer(many=True)
    genre = GenreSerializer()
    rate = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'genre', 'actors', 'release_date', 'rate', 'resume']
    
    def get_rate(self, obj):
        rate = obj.reviews.aggregate(Avg('stars'))['stars__avg']
        if rate:
            return round(rate, 1)
        return None
