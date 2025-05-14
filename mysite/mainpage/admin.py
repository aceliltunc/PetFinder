from django.contrib import admin
from .models import Pet, AdoptionRequest

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'age', 'gender', 'status', 'owner', 'date_posted')
    list_filter = ('species', 'gender', 'status')
    search_fields = ('name', 'breed', 'owner__username')


@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ('pet', 'user', 'request_date')
    search_fields = ('pet__name', 'user__username')
