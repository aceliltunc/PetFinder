from django.contrib import admin
from .models import Pet, Tag, PetSighting, AdoptionRequest, Message

class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'breed', 'age', 'gender', 'status', 'owner', 'date_reported')
    list_filter = ('species', 'status', 'gender')
    search_fields = ('name', 'breed', 'description')
    date_hierarchy = 'date_reported'
    filter_horizontal = ('tags',)
    
    readonly_fields = ('date_reported',)  # ← sadece görüntülenebilir hale getiriyoruz

    fieldsets = (
        ('Hayvan Bilgileri', {
            'fields': ('name', 'species', 'breed', 'age', 'gender', 'image')
        }),
        ('Durum ve Açıklama', {
            'fields': ('status', 'description', 'last_seen_location', 'last_seen_date')
        }),
        ('Sahip Bilgileri', {
            'fields': ('owner',)
        }),
        ('Diğer Bilgiler', {
            'fields': ('tags',)  # ← BURADAN date_reported ALINDI
        }),
        ('Rapor Tarihi (Sadece Görüntüleme)', {
            'fields': ('date_reported',)  # ← Burada sadece readonly olarak görüntülenebilir
        }),
    )


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class PetSightingAdmin(admin.ModelAdmin):
    list_display = ('pet', 'location', 'date_seen', 'user', 'created_at')
    list_filter = ('date_seen',)
    search_fields = ('location', 'notes')

class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ('pet', 'user', 'request_date')
    list_filter = ('request_date',)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp', 'is_read')
    list_filter = ('timestamp', 'is_read')
    search_fields = ('content',)

admin.site.register(Pet, PetAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(PetSighting, PetSightingAdmin)
admin.site.register(AdoptionRequest, AdoptionRequestAdmin)
admin.site.register(Message, MessageAdmin)