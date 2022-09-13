import email
from email import message
from random import randint
from urllib import request

from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, mixins, status, viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from reviews.models import Category, Genre, Review, Title
from users.models import User

from .permissions import (IsAdminModeratorOwnerOrReadOnly, IsAdminOrReadOnly,
                          IsAuthorOrAdminPermission, AdminOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          RegistrationSerializer, 
                          TokenObtainPairEmailSerializer)

confirmation_dict = {}
TOKENS_DICT = {}


def get_confirmation_code():
    symbols = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890'
    code = ''.join(symbols[randint(0, len(symbols) - 1)] for i in range(6))

    return code

# изменить работу эндпоинтов. токенобтэинпэир только по урлу токен


class TokenObtainPairConfirmEmailView(APIView):
    serializer_class = TokenObtainPairEmailSerializer

    def post(self, request, *args, **kwargs):
        if ('username' not in request.data or
            'confirmation_code' not in request.data):
            message = 'Введите данные'
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        input_username = request.data['username']
        input_confirmation_code = request.data['confirmation_code']
        user = get_object_or_404(User, username=input_username)

        if input_username != user.username:
            message = 'Неправильный логин'
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        if input_confirmation_code != user.confirmation_code:
            message = 'Неправильный код подтверждения'
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        print('token-obtain')

        return Response(user.token, status=status.HTTP_200_OK)


# самостоятельная регистрация пользователя и создание нового п. админов - 2 разных класса
class UserRegistration(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    
    def post(self, serializer):
        user = self.request.data
        confirmation_code = get_confirmation_code()

        try:
            user = get_object_or_404(User, username=user['username'])

            data = {
                'email': user.email,
                'username': user.username
            }
            send_mail(
                'Confirmation code',
                confirmation_code,
                'test@test.com',
                [user.email, ]
            )

            return Response(data, status=status.HTTP_200_OK)
        except:
            serializer = self.serializer_class(data=user)
            serializer.is_valid(raise_exception=True)

            serializer.save(confirmation_code=confirmation_code,)

            data = {
                'email': serializer.validated_data['email'],
                'username': serializer.validated_data['username']
            }

            send_mail(
                'Confirmation code',
                confirmation_code,
                'test@test.com',
                [serializer.validated_data['email'], ]
            )

            return Response(data, status=status.HTTP_200_OK)


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    pagination_class = PageNumberPagination
    permission_classes = (AdminOnly,)
    filter_backends = (SearchFilter,)
    search_filters = ('username',)

    def perform_create(self, serializer):
        if 'role' in self.request.data:
            if self.request.data['role'] == 'moderator':
                serializer.save(is_moderator=True)
            elif self.request.data['role'] == 'admin':
                serializer.save(is_staff=True)
        serializer.save()

    def perform_update(self, serializer):
        if 'role' in self.request.data:
            if self.request.data['role'] == 'moderator':
                serializer.save(is_moderator=True)
            elif self.request.data['role'] == 'admin':
                serializer.save(is_staff=True)
        serializer.save()


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (IsAuthorOrAdminPermission,)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAdminModeratorOwnerOrReadOnly,
    )

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAdminModeratorOwnerOrReadOnly,
    )

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments


class ListCreateDestoyViewSet(mixins.CreateModelMixin,
                              mixins.DestroyModelMixin,
                              mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(ListCreateDestoyViewSet):
    '''
    Обработка запросов на категорий произведений.
    Поддерживаемые HTTP-методы: GET/POST/DELETE.
    '''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestoyViewSet):
    '''
    Обработка запросов на получение/создание/удаление жанров произведений.
    Поддерживаемые HTTP-методы: GET/POST/DELETE.
    '''
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    '''
    Обработка запросов на получение/создание/изменение/удаление произведений.
    Поддерживаемые HTTP-методы: GET/POST/PATCH/DELETE.
    '''
    queryset = (Title.objects.annotate(rating=Avg('reviews__score'))
                .prefetch_related('genre'))
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year',)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve',):
            return TitleReadSerializer
        return TitleWriteSerializer
