from django.contrib import admin
from dogs.models import Country, Breed, Dog, Owner, Hobby
# Register your models here.
@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'breed__id']

@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']    

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'phone_number']      

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['id', 'country']      

@admin.register(Hobby)
class HobbyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name_hobby']   
