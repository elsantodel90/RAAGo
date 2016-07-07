# pylint: disable=invalid-name

import json

from django.test import TestCase

from .test_factories import GameFactory
from .models import Game


class GameQuerySetRatedTests(TestCase):
    ''' Tests for `GameQuerySet.rated` and `unrated` methods. '''

    def setUp(self):
        super(GameQuerySetRatedTests, self).setUp()
        self.game = GameFactory.create()

    @staticmethod
    def _game_as_dict(game):
        ''' JSON game description for errors.'''
        attrs = ['handicap', 'komi', 'result', 'reason', 'points']
        return {attr: getattr(game, attr) for attr in attrs}

    def _assert_rated(self, expected):
        display_expected = 'rated' if expected else 'unrated'
        message = 'Game {} failed. Expected: {}'.format(
            json.dumps(
                self._game_as_dict(self.game),
                indent=1, sort_keys=True
            ), display_expected
        )
        game = Game.objects.filter(pk=self.game.pk)
        self.assertEqual(game.rated().exists(), expected, message)
        self.assertEqual(game.unrated().exists(), not expected, message)

    def _assert_is_rated(self):
        self._assert_rated(True)

    def _assert_is_unrated(self):
        self._assert_rated(False)

    def test_default_is_rated(self):
        self._assert_is_rated()

    def test_valid_handicaps_are_rated(self):
        for handicap in range(0, 10):
            self.game.handicap = handicap
            self.game.save()
            self._assert_is_rated()

    def test_handicap_greater_than_nine_is_unrated(self):
        for handicap in [10, 11, 15, 20]:
            self.game.handicap = handicap
            self.game.save()
            self._assert_is_unrated()

    def test_small_handicap_small_komi_is_rated(self):
        for handicap in [0, 1]:
            for komi in [-19.5, -10.5, -6.5, -0.5, 0.5, 6.5, 10.5, 19.5]:
                self.game.handicap = handicap
                self.game.komi = komi
                self.game.save()
                self._assert_is_rated()

    def test_small_handicap_large_komi_is_unrated(self):
        for handicap in [0, 1]:
            for komi in [-30.5, -25.5, -20.5, 20.5, 25.5, 30.5]:
                self.game.handicap = handicap
                self.game.komi = komi
                self.game.save()
                self._assert_is_unrated()

    def test_large_handicap_small_komi_is_rated(self):
        for handicap in range(2, 10):
            for komi in [-9.5, -6.5, -0.5, 0.5, 6.5, 9.5]:
                self.game.handicap = handicap
                self.game.komi = komi
                self.game.save()
                self._assert_is_rated()

    def test_large_handicap_large_komi_is_unrated(self):
        for handicap in range(2, 10):
            for komi in [-30.5, -20.5, -15.5, -10.5, 10.5, 15.5, 20.5, 30.5]:
                self.game.handicap = handicap
                self.game.komi = komi
                self.game.save()
                self._assert_is_unrated()

    def test_draws_are_unrated(self):
        self.game.result = 'draw'
        self.game.save()
        self._assert_is_unrated()

    def test_both_lose_are_unrated(self):
        self.game.result = 'both_lose'
        self.game.save()
        self._assert_is_unrated()

    def test_non_walkover_wins_are_rated(self):
        for result in ['black', 'white']:
            for reason in ['points', 'resignation', 'timeout', 'other']:
                self.game.result = result
                self.game.reason = reason
                self.game.save()
                self._assert_is_rated()

    def test_walkover_wins_are_unrated(self):
        self.game.reason = 'walkover'
        for result in ['black', 'white']:
            self.game.result = result
            self.game.save()
            self._assert_is_unrated()

    def test_whole_komi_is_unrated(self):
        for komi in range(-5, 5):
            self.game.komi = komi
            self.game.save()
            self._assert_is_unrated()

    def test_game_marked_as_unrated_is_unrated(self):
        self.game.unrated = True
        self.game.save()
        self._assert_is_unrated()
