from django.contrib import admin

from .models import Player, Game


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('pk', 'black_player', 'white_player', 'handicap', 'komi',
                    'result', 'win_reason', 'points')
