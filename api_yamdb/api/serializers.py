from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Comment, Follow, Group, Post, User, Auth

class AuthSerializer(serializers.ModelSerializer):

    class Meta:
        model = Auth
        fields = '__all__'
        validators = []

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Такое имя запрещено')
        return data


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault())
    post = serializers.PrimaryKeyRelatedField(
        read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault())
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = '__all__'
        validators = (
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message=('Подписка на автора оформлена ранее!')
            ),
        )

    def validate(self, data):
        if data['user'] == data['following']:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!')
        return data
