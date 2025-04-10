from rest_framework import serializers

class RestPasswordSerializers(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        password = data.get('new_password')
        confirm = data.get('confirm_password')

        if password != confirm:
            raise serializers.ValidationError({"error": "Passwords do not match."})

        return data

    def save(self, user):
        user.set_password(self.validated_data['new_password'])
        user.save()