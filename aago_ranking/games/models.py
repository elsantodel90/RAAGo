import math

from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from model_utils.models import TimeStampedModel


class Player(TimeStampedModel):
    name = models.CharField(max_length=255)
    is_aago_member = models.BooleanField()

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


def _fractional_part(value):
    return value - math.floor(value)


def validate_whole_halfs(value):
    if not _fractional_part(value) in [0, 0.5]:
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
    points = models.DecimalField(
        max_digits=10, decimal_places=1,
        validators=[validate_whole_halfs],
        default=0
    )
    unrated = models.BooleanField(default=False)

    objects = GameQuerySet.as_manager()

    class Meta(object):  # pylint: disable=too-few-public-methods
        verbose_name = 'game'
        verbose_name_plural = 'games'

    def __str__(self):
        return u"{s.white_player} vs {s.black_player} ({s.date})".format(s=self)

    def _validate_reason_in(self, *options):
        if self.reason not in options:
            reasons = dict(_REASON_CHOICES)
            values = ", ".join(str(reasons[o]) for o in options)
            raise ValidationError({'reason': _('Must be one of: %(values)s') % {'values': values}})

    def clean(self):
        if self.handicap == 1:
            self.handicap = 0

        if self.white_player == self.black_player:
            raise ValidationError(_('Black and white players cannot be the same'))

        if self.result == 'draw':
            self._validate_reason_in('points', 'other')
        elif self.result == 'both_lose':
            self._validate_reason_in('walkover', 'other')
        elif self.result == 'null_match':
            self._validate_reason_in('other')

        if self.result in ['white', 'black'] and self.reason == 'points':
            if self.points <= 0:
                raise ValidationError({'points': _('Points must be positive')})
            if _fractional_part(self.komi) != _fractional_part(self.points):
                message = _('Komi and points must have the same fractional value')
                raise ValidationError({'komi': message, 'points': message})
        elif self.points != 0:
            raise ValidationError({'points': _('Points must be 0')})

        if self.event:
            if not self.event.start_date <= self.date <= self.event.end_date:
                raise ValidationError({'date': _('Date is outside event date range')})

            if not self.event.eventplayer_set.filter(player=self.black_player).exists():
                raise ValidationError({'black_player': _('Player does not belong to the event')})
            if not self.event.eventplayer_set.filter(player=self.white_player).exists():
                raise ValidationError({'white_player': _('Player does not belong to the event')})
