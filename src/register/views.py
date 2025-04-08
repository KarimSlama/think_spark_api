from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

from .login_serializers import LoginSerializers
from .models import Profile
from .register_serializers import RegisterSerializers

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .register_serializers import RegisterSerializers

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import Profile

@api_view(['POST'])
def register(request):
    serializer = RegisterSerializers(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        user = User.objects.get(username=request.data['username'])
        profile = Profile.objects.get(user=user)
        refresh = RefreshToken.for_user(user)

        return Response({
            "status": "success",
            "code": 201,
            "message": "User registered successfully",
            "user": {
                "username": user.username,
                "email": user.email,
                "phone": profile.phone,
                "user_type": profile.user_type,
                "is_verified": profile.is_verified,
                "created_at": profile.created_at,
                "token": str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)

    return Response({
        "status": "fail",
        "code": 400,
        "message": "Validation error",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    serializers = LoginSerializers(data=request.data)

    if serializers.is_valid():
        validated_data = serializers.validated_data
        user = validated_data.pop("user")

        return Response({
            "user": {
                "username": validated_data["username"],
                "email": validated_data["email"],
                "phone": validated_data["phone"],
                "token": validated_data["access"],
                "is_verified": validated_data["is_verified"],
                "user_type": validated_data["user_type"],
                "created_at": validated_data["created_at"],
            }
        }, status=status.HTTP_200_OK)

    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)