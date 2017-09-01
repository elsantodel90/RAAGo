#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division
from io import TextIOWrapper

from . import fileloader
import django.utils.encoding

from aago_ranking.events.models import Event, EventPlayer
from aago_ranking.games.models import Player, Game

EVENT_FILE_ENCODING = "latin-1"

class InvalidCategoryError(Exception):
    def __init__(self, message):
        super().__init__(message)

class NonexistentPlayerError(Exception):
    def __init__(self, message):
        super().__init__(message)


def translate_ranking(ranking):
    if ranking.upper().endswith("KYU"):
        return ranking[:-3].strip() + "k"
    elif ranking.upper().endswith("DAN"):
        return ranking[:-3].strip() + "d"
    else:
        raise InvalidCategoryError("Invalid category: " + ranking)

def translate_player(player_name):
    try:
        return Player.objects.get(name=player_name)
    except Player.DoesNotExist:
        raise NonexistentPlayerError("Player named '" + player_name + "' does not exist.")

def upload_event_file(event_file):
    try:
        event_data = fileloader.loadEventFile(TextIOWrapper(event_file.file, encoding=EVENT_FILE_ENCODING))
        for i, p in enumerate(event_data[1]):
            assert p["id"] == i
        for i, r in enumerate(event_data[2]):
            assert r["id"] == i
        for event_round in event_data[2]:
            if "date" not in event_round:
                for round_game in event_round["games"]:
                    if "date" not in round_game:
                        raise fileloader.InvalidEventFileError("A game in round " + str(event_round["id"]) + 
                                                               " has no date. If the round itself has no date, then all of its games must have a date.")
        player_list = [ (translate_player(player["Name"]) , translate_ranking(player["Category"]))  for player in event_data[1]]
        event = Event.objects.create(name       = event_data[0]["Name"],
                                     start_date = event_data[0]["StartDate"],
                                     end_date   = event_data[0]["EndDate"],
                                    )
        for player, rank  in player_list:
            EventPlayer.objects.create(event = event, player = player, ranking = rank)
        for event_round in event_data[2]:
            round_date = event_round.get("date")
            for round_game in event_round["games"]:
                if "date" in round_game:
                    game_date = round_game["date"]
                else:
                    game_date = round_date
                Game.objects.create(event        = event,
                                    date         = game_date,
                                    black_player = player_list[round_game["black_player"]][0],
                                    white_player = player_list[round_game["white_player"]][0],
                                    handicap     = 0,
                                    komi         = 6.5,
                                    result       = round_game["result"],
                                    reason       = "unknown",
                                   )
            
        return {"success" : True}
    except (fileloader.InvalidEventFileError, InvalidCategoryError, NonexistentPlayerError) as e:
        return {"error" : "Invalid event file: " + event_file.name , "error_detail" : str(e)}

