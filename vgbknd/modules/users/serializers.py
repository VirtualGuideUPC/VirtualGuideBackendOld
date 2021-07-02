from vgbknd.modules.places.serializers import NearbyPlaceSerializer
from rest_framework import serializers
from .models import *

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'password', 'name', 'last_name', 'birthday', 'country'] 
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = ['touristic_place', 'user']
    
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

class FavouriteTpSerializer(serializers.ModelSerializer):
    touristic_place_detail = serializers.SerializerMethodField('get_tp')

    class Meta:
        model = Favourite
        fields = [ 'user', 'touristic_place_detail']
    
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

    def get_tp(self, obj):
        tp = obj.touristic_place.touristicplace_id
        tplace = TouristicPlace.objects.filter(touristicplace_id=tp).first()
        serializer = NearbyPlaceSerializer(tplace)
        return str(serializer)

class PreferenceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PreferenceCategory
        fields = ['category', 'user', 'status']
    
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        instance.category = validated_data.get('category', instance.category)
        instance.user = validated_data.get('user', instance.user)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

class PreferenceTypePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreferenceTypePlace
        fields = ['type_place', 'user', 'status']
    
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        instance.type_place = validated_data.get('category', instance.type_place)
        instance.user = validated_data.get('user', instance.user)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


