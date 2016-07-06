#!/usr/bin/env python
# -*- coding: utf-8 -*-o
import datetime

import factory


class PlayerFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'games.Player'

    name = factory.Sequence(lambda n: "Name {}".format(n))


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
