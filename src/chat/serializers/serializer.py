from rest_framework import serializers
from django.contrib.auth.models import User
from chat.models import Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    bio = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'image', 'bio']
    
    def get_image(self, obj):
        if hasattr(obj, 'profile') and obj.profile.image:
            return obj.profile.image.url
        return None
    
    def get_bio(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.bio
        return None

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'text', 'timestamp', 'is_read']


class ConversationDetailSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    participant = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'messages', 'participant']  
    
    def get_participant(self, obj):
        request = self.context.get('request')
        current_user = request.user
        other = obj.participants.exclude(id=current_user.id).first()
        
        return {
            'id': other.id,
            'username': other.username,
            'image': other.profile.image.url if hasattr(other, 'profile') and other.profile.image else None,
            'bio': other.profile.bio if hasattr(other, 'profile') else None,
            'is_online': other.userstatus.is_online if hasattr(other, 'userstatus') else False,
        } if other else None
