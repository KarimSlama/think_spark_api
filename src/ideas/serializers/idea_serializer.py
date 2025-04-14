from rest_framework import serializers
from preferences.serializers.preferences_serializer import PreferencesSerializer
from ..models import Idea, Preferences

class IdeaSerializer(serializers.ModelSerializer):

    categories = PreferencesSerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(queryset=Preferences.objects.filter(type='category'), many=True, write_only=True)

    class Meta:
        model = Idea
        fields = [
            'id',
            'title',
            'categories',        
            'category_ids',      
            'publisher',
            'location',
            'problems',
            'solutions',
            'why_it_works',
            'benifits',
            'image',
            'created_at',
        ]

    def create(self, validated_data):
        category_ids = validated_data.pop('category_ids', [])
        idea = Idea.objects.create(**validated_data)
        idea.categories.set(category_ids)
        return idea