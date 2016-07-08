#!/usr/bin/env python
# -*- coding: utf-8 -*-o
# pylint: disable=too-few-public-methods
import datetime

import factory


class PlayerFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'games.Player'

    name = factory.Sequence("Name {}".format)
    is_aago_member = True


class GameFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'games.Game'

    black_player = factory.SubFactory('aago_ranking.games.test_factories.PlayerFactory')
    white_player = factory.SubFactory('aago_ranking.games.test_factories.PlayerFactory')
    date = datetime.date(2016, 1, 1)

    handicap = 0
    komi = 6.5
    result = 'black'
    reason = 'points'
    points = 5.5
