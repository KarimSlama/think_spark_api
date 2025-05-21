from rest_framework import serializers
from django.contrib.auth.models import User
from register.models import Profile

class InvestorListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = Profile
        fields = ['id', 'username', 'email', 'image', 'bio']
