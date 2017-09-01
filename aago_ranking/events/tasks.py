#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division
from io import TextIOWrapper

from . import fileloader
import django.utils.encoding

EVENT_FILE_ENCODING = "latin-1"

def upload_event_file(event_file):
    try:
        event_data = fileloader.loadEventFile(TextIOWrapper(event_file.file, encoding=EVENT_FILE_ENCODING))
        from aago_ranking.events.models import Event, EventPlayer
        Event.objects.create(name       = event_data[0]["Name"],
                             start_date = event_data[0]["StartDate"],
                             end_date   = event_data[0]["EndDate"],
                            )
        return {"success" : True}
    except fileloader.InvalidEventFileError as e:
        return {"error" : "Invalid event file: " + event_file.name , "error_detail" : str(e)}
    

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
    for game in event.games.rated():
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

    ratings_data = {}
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
        ratings_data[str(player_id)] = {
            "name": player.name,
            "mu": mu,
            "sigma": sigma,
        }
    return ratings_data


def run_ratings_update():
    from aago_ranking.games.models import Player
    from aago_ranking.events.models import Event, EventPlayer
    from .models import PlayerRating
    events = Event.objects.all()
    return {
        str(e.pk): {'name': e.name,
                    'rating_changes': generate_event_ratings(e.pk)}
        for e in events
    }
