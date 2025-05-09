from ideas.serializers.idea_serializer import IdeaSerializer
from preferences.serializers.preferences_serializer import PreferencesSerializer
from preferences.models import Preferences
from ideas.models import Idea
from rest_framework import serializers


class CategoryWithIdeasSerializer(serializers.ModelSerializer):
    ideas = serializers.SerializerMethodField()

    class Meta:
        model = Preferences
        fields = ['id', 'name', 'ideas']

    def get_ideas(self, obj):
        pass
        return IdeaSerializer(
            Idea.objects.filter(categories=obj), many=True
        ).data
