from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.db.models import Avg
from django.utils import timezone
from rest_framework import serializers

from users.constants import MAX_USERNAME_LENGTH
from users.validators import validate_username_me
from reviews.models import Category, Comment, Genre, Review, Title


User = get_user_model()


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
        queryset=Genre.objects.all(), slug_field='slug', many=True
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

    # Нужно сделать валидатор как в signupserializer


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=MAX_USERNAME_LENGTH)
    confirmation_code = serializers.SlugField()


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_USERNAME_LENGTH,
        validators=[validate_username_me, UnicodeUsernameValidator()],
    )
    email = serializers.EmailField(max_length=254)

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def validate(self, data):
        error_msg = {}
        user_with_provided_username = User.objects.filter(
            username=data['username']
        ).first()
        user_with_provided_email = User.objects.filter(
            email=data['email']
        ).first()
        if not user_with_provided_username and not user_with_provided_email:
            User.objects.create(**data)
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
