from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

from register.serializers.profile_serializers import ProfileSerializer

from .serializers.password_reset_request_serializers import PasswordResetRequestSerializer
from .serializers.reset_password_serializers import RestPasswordSerializers
from .serializers.verify_code_reset_request_serializers import VerifyCodeResetRequestSerializers

from .serializers.login_serializers import LoginSerializers
from .models import Profile
from .serializers.register_serializers import RegisterSerializers
from rest_framework.permissions import AllowAny


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializers(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        user = User.objects.get(username=request.data['username'])
        profile = Profile.objects.get(user=user)
        refresh = RefreshToken.for_user(user)

        print("Access Token:", str(refresh.access_token))  # طباعة للتأكد
        print("Refresh Token:", str(refresh))


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
                "refresh": str(refresh),
            }
        }, status=status.HTTP_201_CREATED)

    return Response({
        "status": "fail",
        "code": 400,
        "message": "Validation error",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializers = LoginSerializers(data=request.data)

    if serializers.is_valid():
        validated_data = serializers.validated_data
        user = validated_data.pop("user")

        return Response({
            "status": "success",
            "code": 201,
            "message": "User logged successfully",
            "user": {
                "username": validated_data["username"],
                "email": validated_data["email"],
                "phone": validated_data["phone"],
                "token": validated_data["access"],
                "refresh": validated_data["refresh"],
                "is_verified": validated_data["is_verified"],
                "user_type": validated_data["user_type"],
                "created_at": validated_data["created_at"],
            }
        }, status=status.HTTP_200_OK)

    return Response({
        "status": "fail",
        "code": 400,
        "message": "Validation error",
        "errors": serializers.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def request_password_rest(request):
    
    serializers = PasswordResetRequestSerializer(data=request.data)
    
    if serializers.is_valid():
        result = serializers.save()
        identifier = serializers.validated_data["identifier"]        
        request.session["reset_identifier"] = identifier
        return Response({"message": "Reset Code Sent.", "identifier": identifier}, status=status.HTTP_200_OK)
    
    errors = serializers.errors
    if 'identifier' in errors:
        return Response({"message": errors['identifier'][0]}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "An unknown error occurred."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def verify_code(request):
    identifier = request.data.get('identifier')

    if not identifier:
        return Response({"message": "Identifier is missing!"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = VerifyCodeResetRequestSerializers(
        data=request.data,
        context={'identifier': identifier}
    )

    if serializer.is_valid():
        return Response({"message": "Code verified successfully."}, status=status.HTTP_200_OK)

    return Response({
        "message": serializer.errors.get("non_field_errors", ["Unknown error"])[0]
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def reset_password(request):
    identifier = request.data.get('identifier')

    if not identifier:
        return Response({"error": "Identifier is required."}, status=400)

    try:
        if '@' in identifier:
            user = User.objects.get(email=identifier)
        else:
            profile = Profile.objects.get(phone=identifier)
            user = profile.user
    except:
        return Response({"error": "User not found."}, status=404)

    serializer = RestPasswordSerializers(data=request.data)

    if serializer.is_valid():
        serializer.save(user)
        return Response({"message": "Password reset successfully."}, status=200)

    return Response({"error": serializer.errors.get("error", ["Unknown error"])[0]}, status=400)


@api_view(['GET','PATCH'])
@permission_classes([AllowAny])
def get_user_profile(request):
    profile = request.user.profile
    serializer = ProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully!", "profile": serializer.data}, status=status.HTTP_200_OK)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    