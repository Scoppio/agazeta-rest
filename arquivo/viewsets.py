from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from arquivo.permissions import IsOwnerOrReadOnly, IsOwner
from arquivo.serializers import UserSerializer, TobTokenSerializer, TobTokenSerializerVersion1, MMatchSerializer
from arquivo.services import matchServices, tobTokenServices
from django.shortcuts import get_object_or_404


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
    queryset = tobTokenServices.getAllTobTokens()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.version == 'v1':
            return TobTokenSerializerVersion1
        return TobTokenSerializer


class MatchViewSet(viewsets.ReadOnlyModelViewSet):
    throttle_classes = (UserRateThrottle,)
    permission_classes = (permissions.IsAdminUser,)
    queryset = matchServices.getAllMatches().order_by('match_id')
    serializer_class = MMatchSerializer