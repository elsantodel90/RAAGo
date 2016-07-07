#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division

import io
import logging
import math
import subprocess

from django.conf import settings

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def generate_event_ratings(event_pk):
    from aago_ranking.games.models import Player
    from aago_ranking.events.models import Event, EventPlayer
    from .models import PlayerRating
    event = Event.objects.get(pk=event_pk)
    ratings = PlayerRating.objects.filter(event__lt=event).order_by('-event')
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
        print(
            game.white_player.pk,
            game.black_player.pk,
            game.handicap,
            math.floor(game.komi),
            game.result.upper(),
            file=data
        )
    print('END_GAMES', file=data)

    proc = subprocess.Popen(
        [settings.RAAGO_BINARY_PATH],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = proc.communicate(data.getvalue().encode('utf-8'))
    if proc.wait() != 0:
        raise Exception(
            "Failed execution of raago: '{}'. Exit code: {}. Stderr: '{}'".format(
                settings.RAAGO_BINARY_PATH,
                proc.wait(),
                stderr,
            )
        )

    event.playerrating_set.all().delete()

    json = {}
    for line in stdout.decode('utf-8').splitlines():
        line = line.strip()
        if not line:
            continue
        player_id, mu, sigma = [float(x) for x in line.split()]
        player_id = int(player_id)
        player = Player.objects.get(pk=player_id)
        event.playerrating_set.create(player=player,
                                      mu=mu,
                                      sigma=sigma, )
        json[str(player_id)] = {
            "name": player.name,
            "mu": mu,
            "sigma": sigma,
        }
    return json


def run_ratings_update():
    from aago_ranking.games.models import Player
    from aago_ranking.events.models import Event, EventPlayer
    from .models import PlayerRating
    events = Event.objects.all()
    json = {
        str(e.pk): {'name': e.name,
                    'rating_changes': generate_event_ratings(e.pk)}
        for e in events
    }
    return json
