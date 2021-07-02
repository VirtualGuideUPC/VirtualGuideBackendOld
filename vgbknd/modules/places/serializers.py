from rest_framework import serializers
from .models import *

class TouristicPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TouristicPlace
        fields = ['name', 'cost_info', 'price', 'schedule_info', 'historic_info', 'long_info', 'short_info', 'activities_info', 'latitude', 'longitude', 'tp_range', 'province', 'type_place'] 
    
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance


class PictureTouristicPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PictureTouristicPlace
        fields = ['url', 'number', "touristic_place"] 
    
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

class PictureTpUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = PictureTouristicPlace
        fields = ['url'] 

class TouristicPlaceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TouristicPlaceCategory
        fields = ['category', "touristic_place"] 
    
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance


class CategoryTpSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_name')
    
    class Meta:
        model = TouristicPlaceCategory
        fields = ['category', 'name'] 

    def get_name(self, obj):
        return obj.category.name

class NearbyPlaceSerializer(serializers.ModelSerializer):
    
    province_name = serializers.SerializerMethodField('get_province_name')
    picture = serializers.SerializerMethodField('get_picture')

    class Meta:
        model = TouristicPlace
        fields = ['touristicplace_id', 'name', 'short_info', 'latitude', 'longitude', 'picture','tp_range', 'province_name', 'avg_ranking', 'number_comments'] 

    def get_province_name(self, obj):
        pname = obj.province.name
        return pname
    
    def get_picture(self, obj):
        tp_id = obj.id 
        tppicture = PictureTouristicPlace.objects.filter(touristic_place=tp_id).values('url')
        print("Value: ", tppicture)
        return str(tppicture)
    
 