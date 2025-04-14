from rest_framework import serializers
from preferences.models import Preferences

class PreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preferences
        fields = ['id', 'name', 'type']

    def to_representation(self, instance):
        if instance.type == 'category':
            return super().to_representation(instance)
        return None
