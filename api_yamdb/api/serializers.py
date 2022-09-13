import datetime as dt
from email.policy import default

from django.contrib.auth.hashers import make_password

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from rest_framework_simplejwt.serializers import (TokenObtainPairSerializer,
                                                  PasswordField)

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CHOICES, User


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
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    title = SlugRelatedField(
        slug_field='name',
        read_only=True,
    )

    class Meta:
        fields = '__all__'
        model = Review
        validators = (
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('reviewer', 'title',),
                message='На это произведение Вы уже оставляли отзыв.',),
        )


class TokenObtainPairEmailSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["confirmation_code"] = serializers.CharField()

'''
class UserSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(write_only=True, default='')
    role = serializers.ChoiceField(choices=CHOICES, default='user')
    password = serializers.CharField(write_only=True, default=None)

    class Meta:
        fields = ('username', 'email', 'first_name', 'is_active',
                  'last_name', 'bio', 'role', 'password', 'confirmation_code',)
        model = User
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('email', 'username', 'password', 'confirmation_code'),
                message='Такое название уже занято'
            )
        ]

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        
        # Adding the below line made it work for me.
        instance.is_active = True
        if password is not None:
            # Set password does the hash, so you don't need to call make_password 
            instance.set_password(password)
        print('hey')
        instance.save()
        return instance

    def validate(self, data):
        if data['email'] == data['username']:
            raise serializers.ValidationError(
                'Почта не может совадать с именем')
        elif data['username'] == 'me':
            raise serializers.ValidationError(
                'Имя не может быть равно me')
        return data

    def validate_password(self, value):
        return make_password(value)'''


class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """

    username = serializers.CharField(max_length=128, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        default=''
    )
    confirmation_code = serializers.CharField(write_only=True, default='')
    role = serializers.ChoiceField(choices=CHOICES, default='user')

    class Meta:
        model = User
        fields = ['email', 'username', 'password',
                  'confirmation_code', 'bio',
                  'first_name', 'last_name', 'role']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate(self, data):
        if data['email'] == data['username']:
            raise serializers.ValidationError(
                'Почта не может совадать с именем')
        elif data['username'] == 'me':
            raise serializers.ValidationError(
                'Имя не может быть равно me')
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
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        return obj.rating

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
        return instance

    class Meta:
        model = Title
        fields = '__all__'
