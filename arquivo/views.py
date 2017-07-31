from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def account_profile(request):
    return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def analytics(request):
    return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def matchList(request, page):
    throttle_classes = (UserRateThrottle,)



    # class CardViewSet(mViewsets.ReadOnlyModelViewSet):
    #     """
    #     API endpoint that allows users to be viewed or edited.
    #     """
    #     throttle_classes = (UserRateThrottle,)
    #     permission_classes = (permissions.IsAdminUser, IsOwnerOrReadOnly,)
    #     queryset = MCardPlayed.objects
    #     serializer_class = MCardPlayed(queryset)