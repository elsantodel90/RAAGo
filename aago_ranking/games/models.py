from django.db import models

from model_utils.models import TimeStampedModel


class Player(TimeStampedModel, models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return "Player: {s.name}".format(s=self)


class Game(TimeStampedModel, models.Model):
    white_player = models.ForeignKey('Player', db_index=True)
    date = models.DateField(db_index=True)

    class Meta(object):  # pylint: disable=too-few-public-methods
        verbose_name = 'game'
        verbose_name_plural = 'games'

    def __unicode__(self):
        return u"Game: {s.date}".format(s=self)
