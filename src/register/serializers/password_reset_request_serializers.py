import random
from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.mail import send_mail
from project import settings
from register.models import PasswordRestCode, Profile
from twilio.rest import Client

class PasswordResetRequestSerializer(serializers.Serializer):
    identifier = serializers.CharField()

    def validate_identifier(self, value):
        self.user = None
        
        if '@' in value:
            try:
                self.user = User.objects.get(email=value)
            except User.DoesNotExist:    
                raise serializers.ValidationError('No user with this email.')
        
        else: 
            try:
                profile = Profile.objects.get(phone=value)
                self.user = profile.user
            except Profile.DoesNotExist:
                raise serializers.ValidationError('No user with this phone number.')
            
        return value
    
    def create(self, validated_data):
        try:
            code = str(random.randint(1000, 9999))
            PasswordRestCode.objects.create(user=self.user, code=code)

            identifier = validated_data['identifier']

            if '@' in identifier:
                self.send_email(identifier, code)
            else:
                self.send_sms(identifier, code)
            
            return {"message": "Reset Code sent successfully."}
        
        except serializers.ValidationError as e:
            return {"message": str(e)}

    def send_email(self, email, code):
        send_mail(
            subject="Your Password Reset Code",
            message=f"Your reset code associated with Think Spark is: {code}",
            from_email="think-spark@ideas-service.com",
            recipient_list=[email],
        )
        
    def send_sms(self, phone, code):
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"Your reset code is: {code}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone,
        )
