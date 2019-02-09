#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division

import io
import logging
import math
import subprocess
from . import plotter
import os

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
    
    playersWithGames = set()
    print('GAMES', file=data)
    for game in event.games.rated():
        playersWithGames.add(game.white_player.pk)
        playersWithGames.add(game.black_player.pk)
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

    def readRangoOutputLine(line):
        player_id, mu, sigma = line.split()
        return int(player_id), float(mu), float(sigma)

    ratings_data = {}
    for line in stdout.decode('utf-8').splitlines():
        line = line.strip()
        if not line:
            continue
        player_id, mu, sigma = readRangoOutputLine(line)
        if player_id in playersWithGames:
            player = Player.objects.get(pk=player_id)
            event.playerrating_set.create(player=player,
                                          mu=mu,
                                          sigma=sigma, )
            ratings_data[str(player_id)] = {
                "name": player.name,
                "mu": mu,
                "sigma": sigma,
            }
            
    return ratings_data

def converted_mu(x):
    return x + (x<0) - (x>0)

def run_ratings_update():
    from aago_ranking.games.models import Player
    from aago_ranking.events.models import Event, EventPlayer
    from .models import PlayerRating
    events = Event.objects.all()
    ret = {
        str(e.pk): {'name': e.name,
                    'rating_changes': generate_event_ratings(e.pk)}
        for e in events
    }
    for player in Player.objects.all():
        plot_filename = "{}.png".format(player.pk)
        params = [(playerRating.event.end_date.toordinal(), converted_mu(playerRating.mu))
            for playerRating in PlayerRating.objects.filter(player=player).order_by('event')]
        if params:
            plotter.plot_data([p[0] for p in params], [p[1] for p in params] , os.path.join(settings.RAAGO_PLOTS_PATH, plot_filename))
    return ret
