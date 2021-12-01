from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Category, Comments, Genre, Review, Title, User


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')


class NotAdminSerializer(serializers.ModelSerializer):
    """Евгений!"""
    pass


class GetTokenSerializer(serializers.ModelSerializer):
    """Евгений!"""
    class Meta:
        model = User
        fields = (
            'username', 'confirmation_code')


class SignUpSerializer(serializers.ModelSerializer):
    """Готово!"""
    class Meta:
        model = User
        fields = ('email', 'username')


class CategorySerializer(serializers.ModelSerializer):
    """Михаил!"""
    class Meta:
        model = Category
        fields = '__all__'
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Михаил!"""
    class Meta:
        model = Genre
        fields = '__all__'
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    """Михаил!"""
    pass


class TitleWriteSerializer(serializers.ModelSerializer):
    """Михаил!"""
    pass


class ReviewSerializer(serializers.ModelSerializer):
    """Дмитрий!"""
    pass


class CommentsSerializer(serializers.ModelSerializer):
    """Дмитрий!"""
    pass
