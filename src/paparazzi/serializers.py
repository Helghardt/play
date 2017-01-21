from paparazzi.models import Photo
from rest_framework import serializers


class ListCreatePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('image', 'data', 'is_profile')

    def validate(self, validated_data):
        user = self.context['request'].user

        return validated_data

    def create(self, validated_data: dict):
        request = self.context['request']
        instance = Photo.objects.create(**validated_data)

        return instance
