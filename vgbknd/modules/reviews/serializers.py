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
    user_id = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='user_id'
    )


    user_name = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Review
        fields = ['user_id', 'user_name', 'date', 'comment', 'ranking'] 
    
    
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance