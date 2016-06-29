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

    proc = subprocess.Popen([settings.RAAGO_BINARY_PATH],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    stdout = proc.communicate(data.getvalue().encode('utf-8'))[0]
    if proc.wait() != 0:
        raise Exception("Failed execution of raago: '{}'".format(
            settings.RAAGO_BINARY_PATH))

    event.playerrating_set.all().delete()

    json = {}
    for line in stdout.decode('utf-8').splitlines():
        line = line.strip()
        if not line:
            continue
        player_id, mu, sigma = [float(x) for x in line.split()]
        player_id = int(player_id)
        player = Player.objects.get(pk=player_id)
        event.playerrating_set.create(
            player=player,
            mu=mu,
            sigma=sigma,
        )
        playerJson = {}
        playerJson["name"] = player.name
        playerJson["mu"] = mu
        playerJson["sigma"] = sigma
        json[str(player_id)] = playerJson
    return json

def run_ratings_update():
    from aago_ranking.games.models import Player
    from aago_ranking.events.models import Event, EventPlayer
    from .models import PlayerRating
    events = Event.objects.order_by('end_date') # TODO: check, this might not be a total order on the events, duplicate of decision in generate_event_ratings
    json = {}
    for event in events:
        eventJson = {"name" : event.name}
        eventJson["rating_changes"] = generate_event_ratings(event.pk)
        json[str(event.pk)] = eventJson
    return json
