from rest_framework import mixins, permissions, viewsets
from reviews.models import User

from .serializers import UserSerializer


class UsersViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny, )
