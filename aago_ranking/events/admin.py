from django.contrib import admin

from .models import Event, EventPlayer

# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')


@admin.register(EventPlayer)
class EventPlayerAdmin(admin.ModelAdmin):
    list_display = ('event', 'player', 'ranking')
