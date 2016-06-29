from __future__ import unicode_literals

from django.db import models

from model_utils.models import TimeStampedModel

# Create your models here.


class Event(TimeStampedModel):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(default='', blank=True)

    def __str__(self):
        return self.name


_RANKING_CHOICES = (
    ('1d', '1dan'),
    ('2d', '2dan'),
    ('3d', '3dan'),
    ('4d', '4dan'),
    ('5d', '5dan'),
    ('6d', '6dan'),
    ('7d', '7dan'),
    ('8d', '8dan'),
    ('9d', '9dan'),
    ('1k', '1kyu'),
    ('2k', '2kyu'),
    ('3k', '3kyu'),
    ('4k', '4kyu'),
    ('5k', '5kyu'),
    ('6k', '6kyu'),
    ('7k', '7kyu'),
    ('8k', '8kyu'),
    ('9k', '9kyu'),
    ('10k', '10kyu'),
    ('11k', '11kyu'),
    ('12k', '12kyu'),
    ('13k', '13kyu'),
    ('14k', '14kyu'),
    ('15k', '15kyu'),
    ('16k', '16kyu'),
    ('17k', '17kyu'),
    ('18k', '18kyu'),
    ('19k', '19kyu'),
    ('20k', '20kyu'),
    ('21k', '21kyu'),
    ('22k', '22kyu'),
    ('23k', '23kyu'),
    ('24k', '24kyu'),
    ('25k', '25kyu'),
    ('26k', '26kyu'),
    ('27k', '27kyu'),
    ('28k', '28kyu'),
    ('29k', '29kyu'),
    ('30k', '30kyu'),
)  # yapf: disable


class EventPlayer(models.Model):
    event = models.ForeignKey('Event')
    player = models.ForeignKey('games.Player')
    ranking = models.CharField(max_length=4, choices=_RANKING_CHOICES)
