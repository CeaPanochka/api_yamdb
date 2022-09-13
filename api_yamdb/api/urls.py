from django.urls import include, path, re_path
from rest_framework.routers import SimpleRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserRegistration,
                    TokenObtainPairConfirmEmailView, UserDetail, UserList)

v1_router = SimpleRouter()
v1_router.register(
    'titles/(?P<title_id>\\d+)/reviews/(?P<review_id>\\d+)/comments',
    CommentViewSet,
    basename='comments'
)
v1_router.register(
    'titles/(?P<title_id>\\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(r'genres', GenreViewSet, basename='genre')
v1_router.register(r'categories', CategoryViewSet, basename='category')
v1_router.register(r'titles', TitleViewSet, basename='title')


urlpatterns = [
    path('v1/auth/signup/', UserRegistration.as_view(),
         name='user_registration'),
    path('v1/auth/token/', TokenObtainPairConfirmEmailView.as_view(),
         name='get_token'),
    path('v1/users/', UserList.as_view(), name='users_list'),
    re_path(r'users/(?P<username>[\w.@+-]+)', UserDetail.as_view(), name='users_detail'),
    path('v1/users/me/', UserDetail.as_view(), name='users_me'),
    path('v1/', include(v1_router.urls)),
]
