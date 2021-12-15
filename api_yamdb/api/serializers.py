from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import User


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ('email', 'username')
        model = User
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['email', 'username'],
                message='Поля email и username должны быть уникальными'
            )
        ]
    
    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено'
            )
        return value
