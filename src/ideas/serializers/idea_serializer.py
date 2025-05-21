from rest_framework import serializers
from preferences.serializers.preferences_serializer import PreferencesSerializer
from ideas.models import Idea, IdeaDescription, IdeaRequirement, Preferences
from django.contrib.auth.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source='profile.image', read_only=True)
    bio = serializers.CharField(source='profile.bio', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'image', 'bio']

class IdeaSerializer(serializers.ModelSerializer):
    categories = PreferencesSerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Preferences.objects.filter(type='category'),
        many=True,
        write_only=True
    )
    
    user = UserProfileSerializer(read_only=True)
    
    tabs = serializers.SerializerMethodField()
    
    class Meta:
        model = Idea
        fields = [
            'id',
            'title',
            'categories',
            'category_ids',
            'location',
            'idea_images',
            'created_at',
            'user',
            'tabs'
        ]
    
    def get_tabs(self, obj):
        return {
            "description": {
                "problems": obj.description.problems,
                "solutions": obj.description.solutions,
                "why_it_works": obj.description.why_it_works,
                "benifits": obj.description.benifits
            },
            "requirements": {
                "technical": obj.requirements.technical,
                "operational": obj.requirements.operational,
                "team": obj.requirements.team,
                "expected_duration": obj.requirements.expected_duration
            }
        }
    
    def create(self, validated_data):
        category_ids = validated_data.pop('category_ids', [])
        tabs_data = validated_data.pop('tabs', {})
        
        user = self.context['request'].user
        
        description_data = tabs_data.get('description', {})
        description = IdeaDescription.objects.create(
            problems=description_data.get('problems', ''),
            solutions=description_data.get('solutions', ''),
            why_it_works=description_data.get('why_it_works', ''),
            benifits=description_data.get('benifits', '')
        )
        
        requirements_data = tabs_data.get('requirements', {})
        requirements = IdeaRequirement.objects.create(
            technical=requirements_data.get('technical', ''),
            operational=requirements_data.get('operational', ''),
            team=requirements_data.get('team', ''),
            expected_duration=requirements_data.get('expected_duration', '')
        )
        
        idea = Idea.objects.create(
            user=user,
            description=description,
            requirements=requirements,
            **validated_data
        )
        
        idea.categories.set(category_ids)
        return idea
    

    def update(self, instance, validated_data):
        category_ids = validated_data.pop('category_ids', None)
        tabs_data = self.context['request'].data.get('tabs', {})

        instance.title = validated_data.get('title', instance.title)
        instance.location = validated_data.get('location', instance.location)
        instance.save()

        if category_ids is not None:
            instance.categories.set(category_ids)

        if 'description' in tabs_data:
            desc_data = tabs_data['description']
            description = instance.description
            description.problems = desc_data.get('problems', description.problems)
            description.solutions = desc_data.get('solutions', description.solutions)
            description.why_it_works = desc_data.get('why_it_works', description.why_it_works)
            description.benifits = desc_data.get('benifits', description.benifits)
            description.save()

        if 'requirements' in tabs_data:
            req_data = tabs_data['requirements']
            requirements = instance.requirements
            requirements.technical = req_data.get('technical', requirements.technical)
            requirements.operational = req_data.get('operational', requirements.operational)
            requirements.team = req_data.get('team', requirements.team)
            requirements.expected_duration = req_data.get('expected_duration', requirements.expected_duration)
            requirements.save()

        return instance
