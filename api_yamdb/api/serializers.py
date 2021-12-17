from rest_framework import serializers

from reviews.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для view класса EmailConfirmation."""

    class Meta:
        fields = ('email', 'username')
        model = User
    
    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Использовать имя me в качестве username запрещено'
            )
        return value


class TokenSerializer(serializers.Serializer):
    """Сериализатор для view класса GetToken."""
    username = serializers.CharField(max_length=20)
    confirmation_code = serializers.CharField(max_length=30)
    
    def validate(self, data):
        if not User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError(
                'Пользователя с указанным username не существует'
            )
        user = User.objects.get(username=data['username'])
        if user.confirmation_code != data['confirmation_code']:
            raise serializers.ValidationError(
                'Неверный код подтверждения'
            )
        return data
