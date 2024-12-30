from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from rest_framework import serializers

from users.constants import MAX_EMAIL_LENGTH, MAX_USERNAME_LENGTH
from users.validators import validate_forbidden_username
from reviews.models import Category, Comment, Genre, Review, Title


User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(default=None, read_only=True)

    class Meta:
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field="slug",
        many=True,
        allow_null=True,
        allow_empty=True,
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field="slug",
    )

    class Meta:
        model = Title
        fields = (
            'name', 'year', 'description', 'genre', 'category'
        )

    def to_representation(self, instance):
        read_serializer = TitleReadSerializer(instance)
        return read_serializer.data


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        model = Review
        exclude = ("title",)

    def validate(self, data):
        title_id = self.context["view"].kwargs.get("title_pk")
        is_update = self.instance is not None
        if (
            not is_update
            and Review.objects.filter(
                title_id=title_id,
                author=self.context["request"].user,
            ).exists()
        ):
            raise ValidationError("Вы уже оставляли ревью для этой работы.")
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        model = Comment
        exclude = ("review",)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        model = User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_USERNAME_LENGTH,
        validators=(UnicodeUsernameValidator(), validate_forbidden_username),
    )
    confirmation_code = serializers.SlugField()


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_USERNAME_LENGTH,
        validators=[validate_forbidden_username, UnicodeUsernameValidator()],
    )
    email = serializers.EmailField(max_length=MAX_EMAIL_LENGTH)

    def validate(self, data):
        error_msg = {}
        user_with_provided_username = User.objects.filter(
            username=data["username"]
        ).first()
        user_with_provided_email = User.objects.filter(
            email=data["email"]
        ).first()

        if user_with_provided_email != user_with_provided_username:
            if user_with_provided_email:
                error_msg["email"] = ["Пользователь с таким email уже существует."]
            if user_with_provided_username:
                error_msg["username"] = [
                    "Пользователь с таким username уже существует."
                ]

        if error_msg:
            raise ValidationError(error_msg)
        return data
