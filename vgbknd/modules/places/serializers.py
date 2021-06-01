from rest_framework import serializers
from .models import *

class TouristicPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TouristicPlace
        fields = ['name', 'cost_info', 'price', 'schedule_info', 'historic_info', 'long_info', 'short_info', 'activities_info', 'latitude', 'longitude', 'range', 'province', 'type_place'] 
    
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance


class PictureTouristicPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PictureTouristicPlace
        fields = ['url', 'number'] 
    
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance