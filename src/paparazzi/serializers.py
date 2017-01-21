from src.administration import serializers
from src.paparazzi.models import Photo


class ListCreatePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('id', 'user', 'image', 'data', 'in_profile')

    def validate(self, validated_data):
        user = self.context['request'].user
        email = validated_data.get('email')

        return validated_data

    def create(self, validated_data: dict):
        request = self.context['request']
        instance = Photo.objects.create(**validated_data)

        return instance
