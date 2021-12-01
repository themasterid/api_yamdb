import random
import string
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from reviews.models import Review, Title, User
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import AdminModeratorAuthorPermission, AdminOnly
from .serializers import (CommentsSerializer, NotAdminSerializer,
                          ReviewSerializer, UsersSerializer,
                          GetTokenSerializer, SignUpSerializer)
from django.core.mail import send_mail


class ModelMixinSet(CreateModelMixin, ListModelMixin,
                    DestroyModelMixin, GenericViewSet):
    """Готово!"""
    pass


class CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Готово!"""
    pass


class UsersViewSet(viewsets.ModelViewSet):
    """Готово!"""
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, AdminOnly,)
    lookup_field = 'username'
    filter_backends = (SearchFilter, )
    search_fields = ('username', )
    pagination_class = PageNumberPagination

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated, ),
        url_path='me')
    def get_current_user_info(self, request):
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = UsersSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            else:  # А нужен ли он тут?
                serializer = NotAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UsersSerializer(request.user)
        return Response(serializer.data)


class APIGetToken(APIView):
    """Евгений"""
    queryset = User.objects.all()
    serializer_class = GetTokenSerializer
    permission_classes = (IsAuthenticated,)

    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class APISignup(APIView):
    """Евгений"""
    queryset = User.objects.all()
    serializer_class = SignUpSerializer

    def generate_random_string():
        letters = string.ascii_lowercase
        rand_string = ''.join(random.choice(letters) for i in range(8))
        return rand_string

    send_mail(
        'Код подтверждения',
        generate_random_string(),
        'zhenia2509@mail.ru',
        ['to@example.com'],
        fail_silently=False,
    )
    # условие, если админ делает юзера, отправлять код не нужно.
    pass


class CategoryViewSet(ModelMixinSet):
    """Михаил"""
    pass


class GenreViewSet(ModelMixinSet):
    """Михаил"""
    pass


class TitleViewSet(ModelViewSet):
    """Михаил"""
    pass


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = (AdminModeratorAuthorPermission,)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id')
        )
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AdminModeratorAuthorPermission,)

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, title=title)
