from __future__ import unicode_literals

from django.db import models


class PlayerRating(models.Model):
    player = models.ForeignKey('games.Player', db_index=True)
    event = models.ForeignKey('events.Event', db_index=True)
    mu = models.FloatField()
    sigma = models.FloatField()

    class Meta:
        unique_together = ('player', 'event')

    def __str__(self):
        return "Rating for {s.player} at {s.event}: {s.mu}({s.sigma})".format(s=self)
