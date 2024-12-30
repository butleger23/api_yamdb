from django.core.exceptions import ValidationError
from django.db.models import Avg
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


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Title

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
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )

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


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        exclude = ('title',)

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_pk')
        is_update = self.instance is not None
        if not is_update and Review.objects.filter(
            title_id=title_id,
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
