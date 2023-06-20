from django.contrib import admin

from .models import Event, Interested_In_Event, Place, Comment

@admin.register(Place)
class ModelAdmin(admin.ModelAdmin):
    list_display = ('pk', 'creator','venue_name', 'address', 'zip', 'city', 'state', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'city', 'state', 'venue_name')
    search_fields = ('venue_name', 'address')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'description', 'event_pic', 'date', 'place', 'creator', 'created_at', 'updated_at')
    list_filter = ('date', 'created_at', 'updated_at', 'place__city', 'place__state')
    search_fields = ('title', 'description', 'place__venue_name', 'place__city', 'place__state')
    autocomplete_fields = ('place',)
    ordering = ('pk',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('place')
        return queryset

@admin.register(Interested_In_Event)
class ModelAdmin(admin.ModelAdmin):
    list_display = ('event', 'user')
    list_filter = ('event', 'user')
    search_fields = ('event', 'user')

@admin.register(Comment)
class ModelAdmin(admin.ModelAdmin):
    list_display = ('event', 'user')
    list_filter = ('event', 'user')
    search_fields = ('event', 'user')

