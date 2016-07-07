from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

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
    ('null_match', _('Null match')),
)  # yapf: disable

_REASON_CHOICES = (
    ('points', _('Points')),
    ('resignation', _('Resignation')),
    ('walkover', _('Walkover')),
    ('timeout', _('Timeout')),
    ('other', _('Other')),
)  # yapf: disable


class GameQuerySet(models.QuerySet):
    @staticmethod
    def _rated_query():
        query = Q(handicap__range=(0, 9))
        query &= Q(result__in=('black', 'white'))
        query &= ~Q(reason='walkover')
        query &= Q(unrated=False)
        # Fractional komi
        query &= Q(komi__endswith='.5')

        komi_check = Q(handicap__lt=2, komi__range=(-20, 20))
        komi_check |= Q(komi__range=(-10, 10))
        query &= komi_check

        return query

    def rated(self):
        return self.filter(self._rated_query())

    def unrated(self):
        return self.exclude(self._rated_query())


def validate_whole_halfs(value):
    fractional = value % 1
    if not fractional in [0, 0.5]:
        raise ValidationError(_('Value must be whole halfs: %(value)s'), params={'value': value})


class Game(TimeStampedModel):
    event = models.ForeignKey(
        'events.Event', db_index=True,
        related_name='games',
        null=True, blank=True
    )
    date = models.DateField(db_index=True)
    black_player = models.ForeignKey('Player', db_index=True, related_name='games_as_black')
    white_player = models.ForeignKey('Player', db_index=True, related_name='games_as_white')
    description = models.TextField(default='', blank=True)

    handicap = models.PositiveIntegerField()
    komi = models.DecimalField(max_digits=10, decimal_places=1, validators=[validate_whole_halfs])
    result = models.CharField(max_length=16, choices=_RESULT_CHOICES)
    reason = models.CharField(max_length=16, choices=_REASON_CHOICES)
    points = models.DecimalField(max_digits=10, decimal_places=1, validators=[validate_whole_halfs])
    unrated = models.BooleanField(default=False)

    objects = GameQuerySet.as_manager()

    class Meta(object):  # pylint: disable=too-few-public-methods
        verbose_name = 'game'
        verbose_name_plural = 'games'

    def __str__(self):
        return u"{s.white_player} vs {s.black_player} ({s.date})".format(s=self)
