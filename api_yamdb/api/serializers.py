from django.db.models import Avg
from rest_framework import serializers
from django.utils import timezone
from django.core.exceptions import ValidationError

from reviews.models import Category, Genre, Title, Review, Comment


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
        if not obj.reviews.count():
            return None
        return round(
            obj.reviews.aggregate(Avg('score')).get('score_avg', None), 2)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
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
            author=self.context['request'].user
        ).exists():
            raise ValidationError('Вы уже оставляли ревью для этой работы.')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        exclude = ('review',)
