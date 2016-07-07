from django.contrib import admin
from django.forms.widgets import TextInput
from django.db.models import DecimalField

from .models import Player, Game


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    search_fields = ('name', )


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'event', 'black_player', 'white_player', 'handicap', 'komi', 'result', 'reason',
        'points'
    )
    list_filter = ('event', )
    formfield_overrides = {
        DecimalField: {'widget': TextInput(attrs={'step': '0.5', 'type': 'number'})}
    }  # yapf: disable
