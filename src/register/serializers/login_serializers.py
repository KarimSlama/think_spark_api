from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class LoginSerializers(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        errors = {}

        if errors:
            raise serializers.ValidationError(errors)

        user = User.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError({"email": "Email is not in use"})

        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Invalid password"})

        refresh = RefreshToken.for_user(user)
        return {
            "user": user,
            "username": user.username,
            "email": user.email,
            "phone": user.profile.phone,
            "user_type": user.profile.user_type,
            "is_verified": user.profile.is_verified,
            "created_at": user.profile.created_at,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }