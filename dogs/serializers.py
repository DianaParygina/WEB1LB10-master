from rest_framework import serializers

from dogs.models import Breed, Dog, Owner, Hobby, Country

class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = "__all__"

class BreedCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ['id', 'name'] 

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'pictureOwner']

class HobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobby
        fields = ['id', 'name_hobby']      

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'country'] 

class DogListSerializer(serializers.ModelSerializer):
    breed = BreedSerializer(read_only=True)
    owner = OwnerSerializer(read_only=True)
    hobby = HobbySerializer(read_only=True)
    country = CountrySerializer(read_only=True)

    class Meta:
        model = Dog
        fields = ['id', 'name', 'breed','owner', 'hobby', 'country', 'picture']  


class DogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dog
        fields = ['id', 'name', 'breed','owner', 'hobby', 'country', 'picture']


class DogUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dog
        fields = ['id', 'name', 'breed','owner', 'hobby', 'country', 'picture']            