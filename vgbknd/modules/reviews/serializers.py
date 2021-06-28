from rest_framework import serializers
from .models import *

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['comment', 'comment_ranking', 'date', 'ranking', 'touristic_place', 'user'] 
    
    
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

class UserNameListingField(serializers.RelatedField):
    def to_representation(self, value):
        return 'user_name: %s' (value.name)


class ReviewTpSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    def get_images(self, instance):
        return [slider_image.image.url for slider_image in instance.slider_image.all()]


    class Meta:
        model = Review
        fields = ['user.name', 'date', 'comment', 'ranking'] 
    
    
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance