from rest_framework import serializers
from reviews.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        validators = []

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Такое имя запрещено')
        return data
