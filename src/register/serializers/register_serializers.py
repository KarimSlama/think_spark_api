from django.contrib.auth.models import User
from rest_framework import serializers
from register.models import Profile

class RegisterSerializers(serializers.ModelSerializer):
    phone = serializers.CharField(write_only=True, required=True)
    user_type = serializers.ChoiceField(choices=[("creative", "Creative"), ("investor", "Investor")], default="creative")
    is_verified = serializers.BooleanField(default=False, read_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "phone", "user_type", "is_verified"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        errors = {}

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        phone = data.get("phone")

        if not email:
            errors["email"] = 'Email is required'
        if not username:
            errors["username"] = 'Username is required'
        if not phone:
            errors["phone"] = 'Phone is required'
        if not password:
            errors["password"] = 'Password is required'

        if User.objects.filter(username=username).exists():
            errors["username"] = 'Username is already taken'
        if User.objects.filter(email=email).exists():
            errors["email"] = 'Email is already in use'

        if Profile.objects.filter(phone=phone).exists():
            errors["phone"] = 'Phone number is already in use'

        if errors:
            raise serializers.ValidationError(errors)

        return data

    def create(self, validated_data):
        phone = validated_data.pop("phone")
        user_type = validated_data.pop("user_type")
        is_verified = False
        
        user = User.objects.create_user(**validated_data)

        profile = Profile.objects.create(
            user=user,
            phone=phone,
            user_type=user_type,
            is_verified=is_verified,
            created_at=user.date_joined
        )

        return user