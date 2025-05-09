from rest_framework import serializers

from register.models import Profile;

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'username', 'email', 'phone', 'user_type', 'is_verified', 'created_at', 'image', 'bio']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})

        user = instance.user
        user.username = user_data.get('username', user.username)
        user.email = user_data.get('email', user.email)
        user.save()

        instance.phone = validated_data.get('phone', instance.phone)
        instance.user_type = validated_data.get('user_type', instance.user_type)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance