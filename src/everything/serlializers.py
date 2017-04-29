import json
from rest_framework import serializers
from everything.models import Log, Recipe, LogInput, Image


class CreateLogSerializer(serializers.Serializer):
    recipe = serializers.CharField(required=True)
    title = serializers.CharField(required=True)
    text = serializers.CharField(required=False, allow_blank=True)
    rating = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data: dict):
        create_data = validated_data.copy()
        recipe = Recipe.objects.get(slug=create_data['recipe'])
        instance = Log.objects.create(user=create_data['user'], recipe=recipe, title=create_data['title'])
        instance.build(create_data['rating'])
        return instance


class ListLogSerializer(serializers.ModelSerializer):
    title = serializers.CharField(read_only=True)
    data = serializers.SerializerMethodField(source='data')
    created = serializers.CharField(read_only=True)

    class Meta:
        model = Log
        fields = ('title',
                  'data',
                  'created')

    def get_data(self, log):
        log_input = LogInput.objects.get(log=log)
        return {log_input.content_type.model: log_input.content_object.rating}


class ListCreateImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image',)

    def validate(self, validated_data):
        return validated_data

    def create(self, validated_data: dict):
        instance = Image.objects.create(**validated_data)
        return instance