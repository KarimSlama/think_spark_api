from ideas.models import IdeaDescription
from rest_framework import serializers

class IdeaDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdeaDescription
        fields = ['problems', 'solutions', 'why_it_works', 'benifits']
