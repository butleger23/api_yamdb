from django.core.exceptions import ValidationError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['id']
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['id']
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        if value > timezone.now().year:
            raise ValidationError('Вы не можете указать год в будущем времени')
        return value

    def validate_name(self, value):
        if len(value) > 256:
            raise ValidationError(
                'Название произведения не может быть длиннее 256 символов.'
            )
        return value

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews.exists():
            return None
        average_score = reviews.aggregate(Avg('score')).get('score__avg', None)
        return round(average_score, 2) if average_score is not None else None

    def create(self, validated_data):
        if self.initial_data is dict:
            genre_data = self.initial_data.get('genre')
        else:
            genre_data = self.initial_data.getlist('genre')
        genres = Genre.objects.filter(slug__in=genre_data)
        category = self.initial_data.get('category')
        if not Category.objects.filter(slug=category).exists():
            raise ValidationError('No such category')
        category_object = get_object_or_404(Category, slug=category)

        title = Title.objects.create(
            category=category_object, **validated_data
        )
        title.genre.set(genres)
        return title

    def update(self, instance, validated_data):
        if 'genre' in self.initial_data:
            genre_data = self.initial_data.get('genre')
            genres = Genre.objects.filter(slug__in=genre_data)
            instance.genres.clear()
            instance.genres.set(genres)

        if 'category' in self.initial_data:
            category = self.initial_data.get('category')
            if not Category.objects.filter(slug=category).exists():
                raise ValidationError('no such category')
            category_object = get_object_or_404(Category, slug=category)
            instance.category = category_object
        return super().update(instance, validated_data)


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
