from rest_framework import serializers
from .models import *
from modules.users.models import Account

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

    #user_name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['user', 'date', 'comment', 'ranking'] 

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance