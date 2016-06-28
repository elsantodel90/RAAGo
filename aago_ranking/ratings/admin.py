from django.contrib import admin

from .models import PlayerRating


@admin.register(PlayerRating)
class PlayerRatingAdmin(admin.ModelAdmin):
    list_display = ('event', 'player', 'mu', 'sigma')

