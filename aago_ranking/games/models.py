from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel


class Player(TimeStampedModel):
    name = models.CharField(max_length=255)

    def all_games(self):
        return Game.objects.filter(Q(black_player=self) | Q(white_player=self))

    def __str__(self):
        return self.name


_RESULT_CHOICES = (
    ('black', _('Black Wins')),
    ('white', _('White Wins')),
    ('draw', _('Draw')),
    ('both_lose', _('Both lose')),
)

_WIN_REASON_CHOICES = (
    ('points', _('Points')),
    ('resignation', _('Resignation')),
    ('walkover', _('Walkover')),
    ('timeout', _('Timeout')),
    ('other', _('Other')),
)


class Game(TimeStampedModel):
    event = models.ForeignKey('events.Event',
                              db_index=True,
                              related_name='games',
                              null=True)
    date = models.DateField(db_index=True)
    white_player = models.ForeignKey('Player',
                                     db_index=True,
                                     related_name='games_as_white')
    black_player = models.ForeignKey('Player',
                                     db_index=True,
                                     related_name='games_as_black')
    description = models.TextField(default='', blank=True)

    handicap = models.IntegerField()
    komi = models.DecimalField(max_digits=10, decimal_places=1)
    result = models.CharField(max_length=16, choices=_RESULT_CHOICES)
    win_reason = models.CharField(max_length=16, choices=_WIN_REASON_CHOICES)
    points = models.DecimalField(max_digits=10, decimal_places=1)
    unrated = models.BooleanField(default=False)

    class Meta(object):  # pylint: disable=too-few-public-methods
        verbose_name = 'game'
        verbose_name_plural = 'games'

    def __str__(self):
        return u"{s.white_player} vs {s.black_player} ({s.date})".format(s=self)
