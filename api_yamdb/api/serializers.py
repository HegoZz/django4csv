from django.db.models import fields
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import (Category, Comment, Genre, Genre_title,
                            Title, Review, User)


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


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(
        many=True,
        read_only=True
    )
    category = CategorySerializer(
        read_only=False
    )

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title

    def create(self, validated_data):
        category_slug = validated_data['category']
        category = Category.objects.get(slug=category_slug)
        category_name = category.name
        validated_data['category'] = {
            "name": category_name,
            "slug": category_slug
        }
        genre_data = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        # title.category = Category.objects.get(slug=category_slug)
        # title.save()
        for genre_slug in genre_data:
            genre = Genre.objects.get(slug=genre_slug)
            genre_name = genre.name
            validated_data['category'] = {
                "name": genre_name,
                "slug": genre_slug
            }
            Genre_title.objects.create(
                title_id=title, genre_id=genre)
        return title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('text', 'author', 'score', 'pub_date')
        read_only_fields = ('pub_date', )

    def validate_author(self, value):
        user = get_object_or_404(User, username=value)
        title_id = self.context['request'].title_id
        title = Title.objects.get(id=title_id)
        review = title.reviews.all()
        if user in review.author:
            raise serializers.ValidationError(
                'Нельзя оставлять больше одного отзыва на произведение.'
            )
        return value

    def validate_score(self, value):
        if 1 <= value <= 10:
            return value
        raise serializers.ValidationError(
            'Оценка должна быть от 1 до 10.'
        )


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('text', 'author', 'pub_date')
        read_only_fields = ('pub_date', )
