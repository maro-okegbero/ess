from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ess.permissions import IsAdmin
from users.serializers import RegisterSerializer, UserSerializer, CreateUserSerializer, LoginSerializer


@csrf_exempt
@api_view(['POST'])
def register_as_administrator(request):
    """
    register as an admin
    """
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    serializer = UserSerializer(user)
    data = serializer.data
    return Response(data, status=status.HTTP_201_CREATED)


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAdmin])
def create_user_as_admin(request):
    """
    create a user
    """
    serializer = CreateUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    serializer = UserSerializer(user)
    data = serializer.data
    return Response(data, status=status.HTTP_201_CREATED)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    Log a user in using the email and password as the authentication credentials
    """
    data = request.data
    serializer = LoginSerializer(data=data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    return Response(serializer.validated_data, status=status.HTTP_200_OK)
