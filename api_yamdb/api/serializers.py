from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.db.models import Avg
from rest_framework import serializers

from users.constants import MAX_USERNAME_LENGTH
from users.validators import validate_username_me
from reviews.models import Category, Comment, Genre, Review, Title


User = get_user_model()


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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=MAX_USERNAME_LENGTH)
    confirmation_code = serializers.SlugField()


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_USERNAME_LENGTH,
        validators=[validate_username_me, UnicodeUsernameValidator()],
    )
    email = serializers.EmailField(max_length=254)

    def validate(self, data):
        error_msg = {}
        user_with_provided_username = User.objects.filter(
            username=data['username']
        ).first()
        user_with_provided_email = User.objects.filter(
            email=data['email']
        ).first()
        if not user_with_provided_username and not user_with_provided_email:
            pass
        elif user_with_provided_username == user_with_provided_email:
            pass
        elif user_with_provided_username and user_with_provided_email:
            error_msg['username'] = [
                'Пользователь с таким username уже существует.'
            ]
            error_msg['email'] = ['Пользователь с таким email уже существует.']
        elif user_with_provided_email:
            error_msg['email'] = ['Пользователь с таким email уже существует.']
        else:
            error_msg['username'] = [
                'Пользователь с таким username уже существует.'
            ]

        if error_msg:
            raise ValidationError(error_msg)
        return data
