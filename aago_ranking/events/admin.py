from django.contrib import admin

from aago_ranking.games.models import Game

from .models import Event, EventPlayer

# Register your models here.


class EventPlayerInline(admin.TabularInline):
    model = EventPlayer


class EventGameInline(admin.TabularInline):
    model = Game


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    inlines = (EventPlayerInline, EventGameInline)


@admin.register(EventPlayer)
class EventPlayerAdmin(admin.ModelAdmin):
    list_display = ('event', 'player', 'ranking')
