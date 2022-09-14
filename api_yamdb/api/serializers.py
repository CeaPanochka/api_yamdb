import datetime as dt

from rest_framework import serializers
from rest_framework.exceptions import ParseError
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=(
            UniqueValidator(queryset=User.objects.all()),
        ),
        required=True,
    )
    email = serializers.EmailField(
        validators=(
            UniqueValidator(queryset=User.objects.all()),
        )
    )

    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User
        read_only_fields = ('role',)


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=(
            UniqueValidator(queryset=User.objects.all()),
        )
    )
    email = serializers.EmailField(
        validators=(
            UniqueValidator(queryset=User.objects.all()),
        )
    )

    def validate_username(self, value):
        if value.lower() == "me":
            raise serializers.ValidationError("Username 'me' is not valid")
        return value

    class Meta:
        fields = ("username", "email")
        model = User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, data):
        title_id = (
            self.context['request'].parser_context['kwargs']['title_id']
        )
        title = get_object_or_404(Title, id=title_id)
        user = self.context['request'].user
        if (self.context['request'].method == 'POST'
            and Review.objects.filter(author=user, title=title).exists()):
                raise ParseError('Вы уже оставили отзыв, спасибо!')
        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleWriteSerializer(TitleReadSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug')
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug', many=True)
    year = serializers.IntegerField(min_value=0,
                                    max_value=dt.datetime.now().year)

    def to_representation(self, instance):
        serializer = TitleReadSerializer(instance)
        return serializer.data

    class Meta:
        model = Title
        fields = '__all__'
