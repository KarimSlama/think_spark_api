from rest_framework import serializers
from meetings.models import Meeting

class MeetingSerializer(serializers.ModelSerializer):
    idea_title = serializers.CharField(source='idea.title', read_only=True)
    creative = serializers.CharField(source='idea.user.username', read_only=True)
    investor = serializers.CharField(source='investor.username', read_only=True)
    image = serializers.ImageField(source='idea.user.profile.image', read_only=True)
    
    class Meta:
        model = Meeting
        fields = [
            'id', 'idea', 'investor', 'image',
            'idea_title', 'creative', 'investor',
            'scheduled_datetime', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']     