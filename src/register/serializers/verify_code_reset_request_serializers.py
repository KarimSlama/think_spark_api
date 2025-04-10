from rest_framework import serializers
from register.models import PasswordRestCode, Profile
from django.contrib.auth.models import User 

class VerifyCodeResetRequestSerializers(serializers.Serializer):
    code = serializers.CharField()

    def validate(self, data):
        code = data['code']
        identifier = self.context.get('identifier')

        if not identifier:
            raise serializers.ValidationError('Identifier is missing!')

        try:
            if '@' in identifier:
                user = User.objects.get(email=identifier)
            else:
                profile = Profile.objects.get(phone=identifier)
                user = profile.user
        except (User.DoesNotExist, Profile.DoesNotExist):
            raise serializers.ValidationError('User not found!')

        try:
            reset_code = PasswordRestCode.objects.filter(user=user, code=code).latest('created_at')
        except PasswordRestCode.DoesNotExist:
            raise serializers.ValidationError('Invalid code.')

        if reset_code.is_expired():
            raise serializers.ValidationError('Code expired.')

        data['user'] = user
        return data