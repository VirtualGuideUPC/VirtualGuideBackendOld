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

class PreferenceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PreferenceCategory
        fields = ['category', 'user', 'picture']
    
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

class PreferenceTypePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreferenceTypePlace
        fields = ['type_place', 'user', 'picture']
    
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance