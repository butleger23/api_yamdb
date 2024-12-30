from django.core.exceptions import ValidationError
from django.db.models import Avg
from django.utils import timezone
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if isinstance(representation['genre'], list):
            representation['genre'] = [
                {
                    'name': (
                        genre['name'] if isinstance(genre, dict) else genre
                    ),
                    'slug': (
                        genre['slug'] if isinstance(genre, dict) else genre
                    )
                } for genre in representation['genre']
            ]
        else:
            raise ValueError("Expected 'genre' to be a list of dictionaries.")

        if isinstance(representation['category'], dict):
            representation['category'] = {
                'name': representation['category']['name'],
                'slug': representation['category']['slug']
            }
        else:
            representation['category'] = {'name': None, 'slug': None}

        return representation

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews.exists():
            return None
        average_score = reviews.aggregate(Avg('score')).get('score__avg', None)
        return round(average_score, 2) if average_score is not None else None


class TitleWriteSerializer(TitleReadSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        allow_null=True,
        allow_empty=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        exclude = ('title',)

    def validate_score(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError('Должно быть целое число!')
        if not (1 <= value <= 10):
            raise serializers.ValidationError('Рейтинг должен быть от 1 до 10')
        return value

    def validate(self, data):
        if Review.objects.filter(
            title_id=self.context['view'].kwargs.get('title_id'),
            author=self.context['request'].user,
        ).exists():
            raise ValidationError('Вы уже оставляли ревью для этой работы.')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        exclude = ('review',)
