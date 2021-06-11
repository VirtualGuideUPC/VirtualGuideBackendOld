from rest_framework import serializers
from .models import *

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['comment', 'comment_ranking', 'date', 'models', 'ranking', 'touristic_place', 'user'] 
    
    
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance