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
    my_field = serializers.SerializerMethodField('is_named_bar')

    def is_named_bar(self, foo):
        return foo.name == "bar" 

    class Meta:
        model = Review
        fields = ['my_field', 'date', 'comment', 'ranking'] 

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance