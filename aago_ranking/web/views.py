# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

from aago_ranking.ratings.models import PlayerRating

import datetime
import calendar

def monthsAgo(months, date):
    assert months >= 0
    def days(month, year):
        return calendar.monthrange(year, month)[1]
    day, month, year = date.day, date.month, date.year
    month -= months
    while month < 1:
        month += 12
        year -= 1
    day = min(day, days(month, year))
    return datetime.date(year, month, day)

def ratingIsValid(r):
    anYearAgo = monthsAgo(12, datetime.date.today())
    return r.player.is_aago_member or anYearAgo <= r.event.end_date

def category(mu, provisional):
    if provisional:
        suffix = "?"
    else:
        suffix = ""
    if mu > 0:
        return "{}D{}".format(1+int(mu), suffix)
    else:
        return "{}K{}".format(1+int(-mu), suffix)

def formatRating(mu, sigma):
    return "{:.3f} ± {:.3f}".format(mu, sigma)

def convertRatingToNewConvention(mu):
    # Se elimina el "gap" famoso en (-1, 1)
    if mu <= -1.0:
        return mu + 1.0
    elif mu >= 1.0:
        return mu - 1.0
    else:
        assert False

def get_sorted_ratings():
    ratings = PlayerRating.objects.order_by('event')
    # Note: this query retrieves *every* rating from the DB.
    #   It can be optimized if needed.
    last_ratings = {r.player: (convertRatingToNewConvention(r.mu), r.sigma, r.event.end_date) for r in ratings if ratingIsValid(r)}
    
    scoreboard = sorted(last_ratings.items(), reverse=True, key=(lambda item: item[1][0]))
    active_deadline = monthsAgo(6, datetime.date.today())
    next_rank = 1
    for i, (player,(mu, sigma, last_event_date)) in enumerate(scoreboard):
        rated_games = len(player.all_games().rated())
        css_classes = []
        provisional = False
        if player.is_aago_member:
            css_classes.append("jugador-socio")
        if last_event_date < active_deadline:
            ranking = "―"
            css_classes.append("jugador-inactivo")
        if rated_games < 10:
            css_classes.append("jugador-provisional")
            provisional = True
            ranking = "―"
        if last_event_date >= active_deadline and rated_games >= 10:
            ranking = str(next_rank)
            next_rank += 1
        scoreboard[i] = (ranking, player, rated_games, formatRating(mu, sigma), category(mu, provisional), last_event_date.strftime("%d/%m/%Y"), " ".join(css_classes))
    return scoreboard

def homepage(request):
    return render(request, 'pages/home.html', {'sorted_ratings': get_sorted_ratings(), })

def csv_ranking(request):
    lines = ["Ranking;Socio;Jugador;Partidas;Rating;Categoría;Última participación"]
    lines += ["{};{};{};{};{};{};{}".format(ranking, ("SI" if player.is_aago_member else "NO") , player.name, rated_games, rating, category, last_event_date) for ranking, player, rated_games, rating, category, last_event_date,  _css_classes in get_sorted_ratings()]
    lines.append("") # To get the last end of file character when joining
    return HttpResponse("\r\n".join(lines), content_type='text/plain; charset=utf-8')
    
