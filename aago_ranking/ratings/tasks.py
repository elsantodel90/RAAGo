#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division

import io
import logging
import math
import subprocess

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

# TODO: move to settings
RAAGO_BINARY = 'original-AGA-rating-system/aago-rating-calculator/raago'


def generate_event_ratings(event_pk):
    from aago_ranking.games.models import Player
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

    proc = subprocess.Popen([RAAGO_BINARY],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    stdout = proc.communicate(data.getvalue().encode('utf-8'))[0]
    if proc.wait() != 0:
        return

    event.playerrating_set.all().delete()

    for line in stdout.decode('utf-8').splitlines():
        line = line.strip()
        if not line:
            continue
        player_id, mu, sigma = [float(x) for x in line.split()]
        player = Player.objects.get(pk=player_id)
        event.playerrating_set.create(
            player=player,
            mu=mu,
            sigma=sigma,
        )
