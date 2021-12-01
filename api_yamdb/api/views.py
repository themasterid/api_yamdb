from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from reviews.models import Category, Genre, Review, Title, User
from .permissions import AdminOnly
from .serializers import  NotAdminSerializer, UsersSerializer
from .serializers import UserSerializer
from rest_framework import mixins, permissions, viewsets
from reviews.models import User


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
    pass


class APISignup(APIView):
    """Евгений"""
    # тут прорешать отправку сообщений на мыло,
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
    """Дмитрий"""
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    """Дмитрий"""
    pass
