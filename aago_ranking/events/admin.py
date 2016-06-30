from django.contrib import admin
from django.forms.widgets import Textarea
from django.db.models import TextField

from aago_ranking.games.models import Game

from .models import Event, EventPlayer

# Register your models here.


class EventPlayerInline(admin.TabularInline):
    model = EventPlayer
    extra = 0


class EventGameInline(admin.TabularInline):
    model = Game
    extra = 1
    formfield_overrides = {
        TextField: {'widget': Textarea(attrs={'rows': 1})}
    }


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    inlines = (EventPlayerInline, EventGameInline)
    formfield_overrides = {
        TextField: {'widget': Textarea(attrs={'rows': 2})}
    }


@admin.register(EventPlayer)
class EventPlayerAdmin(admin.ModelAdmin):
    list_display = ('event', 'player', 'ranking')
