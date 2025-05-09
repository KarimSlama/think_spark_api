from ideas.models import IdeaRequirement
from rest_framework import serializers

class IdeaRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdeaRequirement
        fields = ['technical', 'operational', 'team', 'expected_duration']
