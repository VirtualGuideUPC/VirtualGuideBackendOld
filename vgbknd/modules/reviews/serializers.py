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


class ReviewTpSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField('get_user_name')

    class Meta:
        model = Review
        fields = ['user_name', 'date', 'comment', 'ranking'] 

    def get_user_name(self, obj):
        return obj.account.name