import json
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.throttling import UserRateThrottle
from .permissions import IsOwnerOrReadOnly, IsOwner
from .serializers import UserSerializer, TobTokenSerializer, TobTokenSerializerVersion1
from .models import TobToken
from .documents import MMatch, MCardPlayed

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    throttle_classes = (UserRateThrottle,)
    permission_classes = (permissions.IsAdminUser, IsOwner,)
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class TobTokenViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tokens to be viewed or edited.
    """
    throttle_classes = (UserRateThrottle,)
    permission_classes = (permissions.IsAdminUser,)
    queryset = TobToken.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.version == 'v1':
            return TobTokenSerializerVersion1
        return TobTokenSerializer
#
#
# class MatchViewSet(mViewsets.ReadOnlyModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     throttle_classes = (UserRateThrottle,)
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
#     queryset = MMatch.objects
#     serializer_class = MMatchSerializer(queryset)
#
#
# class CardViewSet(mViewsets.ReadOnlyModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     throttle_classes = (UserRateThrottle,)
#     permission_classes = (permissions.IsAdminUser, IsOwnerOrReadOnly,)
#     queryset = MCardPlayed.objects
#     serializer_class = MCardPlayed(queryset)