import json
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import TobToken
from .services import createUserFromTobToken

@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def account_profile(request):
	return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def analytics(request):
    return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

