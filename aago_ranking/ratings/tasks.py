#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division

import logging
import io
import math

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def generate_event_ratings(event_pk):
    from aago_ranking.events.models import Event, EventPlayer
    from .models import PlayerRating
    event = Event.objects.get(pk=event_pk)
    # TODO: check, this might not be a total order on the events
    ratings = PlayerRating.objects.filter(
        event__end_date__lt=event.end_date).order_by('-event__end_date')
    event_players = EventPlayer.objects.filter(event=event)
    data = io.StringIO()

    print('PLAYERS', file=data)
    for event_player in event_players:
        last_rating = ratings.filter(player=event_player.player).first()
        print(event_player.player.pk, event_player.ranking, file=data, end=' ')
        if last_rating:
            rating_age = (event.end_date - last_rating.event.end_date).days
            print(last_rating.mu, last_rating.sigma, rating_age, file=data)
        else:
            print("NULL", "NULL", "NULL", file=data)

    print('END_PLAYERS', file=data)
    print('GAMES', file=data)
    for game in event.games.all():
        print(game.white_player.pk,
              game.black_player.pk,
              game.handicap,
              math.floor(game.komi),
              game.result.upper(),
              file=data)
    print('END_GAMES', file=data)
    return data.getvalue()
