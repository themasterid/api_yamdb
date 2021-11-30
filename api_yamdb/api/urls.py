from django.urls import include, path
from rest_framework.routers import SimpleRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
<<<<<<< HEAD

# TODO Как будут готовы раскомментить.
# from .views import (APIGetToken, APISignup, CategoryViewSet, CommentsViewSet,
#                    GenreViewSet, ReviewViewSet, TitleViewSet, UsersViewSet)

app_name = 'api'

router = SimpleRouter()
"""
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)
router.register(
    'users',
    UsersViewSet,
    basename='users'
)
router.register(
    'categories',
    CategoryViewSet,
    basename='сategories'
)
router.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
router.register(
    'genres',
    GenreViewSet,
    basename='genres'
)
"""
=======
from .views import AuthViewSet, UserViewSet
# from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

router = DefaultRouter()
# router.register('posts', PostViewSet)
# router.register('groups', GroupViewSet)
# router.register('follow', FollowViewSet, basename='followers')
# router.register(r'^posts/(?P<post_id>\d+)/comments',
#                 CommentViewSet, basename='comments')
router.register('users', UserViewSet)

>>>>>>> feature/develop

urlpatterns = [
    # path('v1/auth/token/', APIGetToken.as_view(), name='get_token'),
    path('v1/', include(router.urls)),
<<<<<<< HEAD
    # path('v1/auth/signup/', APISignup.as_view(), name='signup'),
=======
    path(
        'v1/token/', TokenObtainPairView.as_view(),
        name='token_obtain_pair'),
    path(
        'v1/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'),
    path(
        '/v1/auth/signup/',
        AuthViewSet.as_view(),
        name='auth_signup'),
>>>>>>> feature/develop
]
