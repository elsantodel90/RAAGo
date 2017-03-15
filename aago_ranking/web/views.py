from django.shortcuts import render
from django.http import HttpResponse

from aago_ranking.ratings.models import PlayerRating

import datetime

def ratingIsValid(r):
    # We do not care about leap years at all for these purposes
    anYearAgo = datetime.date.today() - datetime.timedelta(days=365)
    return r.player.is_aago_member or anYearAgo < r.event.end_date

def category(mu):
    if mu > 0:
        return "{}D".format(int(mu))
    else:
        return "{}K".format(int(-mu))

def get_sorted_ratings():
    ratings = PlayerRating.objects.order_by('event')
    # Note: this query retrieves *every* rating from the DB.
    #   It can be optimized if needed.
    last_ratings = {r.player: (r.mu, r.event.end_date) for r in ratings if ratingIsValid(r)}
    
    scoreboard = sorted(last_ratings.items(), reverse=True, key=(lambda item: item[1][0]))
    active_deadline = datetime.date.today() - datetime.timedelta(days=185)
    next_rank = 1
    for i, (player,(mu, last_event_date)) in enumerate(scoreboard):
        rated_games = len(player.all_games().rated())
        if last_event_date < active_deadline:
            ranking = "(inactivo)"
        elif rated_games < 10:
            ranking = "(provisional)"
        else:
            ranking = str(next_rank)
            next_rank += 1
        scoreboard[i] = (ranking, player, mu, category(mu) , rated_games)
    return scoreboard

def homepage(request):
    return render(request, 'pages/home.html', {'sorted_ratings': get_sorted_ratings(), })

def csv_ranking(request):
    lines = ["Ranking;Socio;Jugador;Rating;Categoría;Partidas"]
    lines += ["{};{};{};{:.3f};{};{}".format(ranking, ("SI" if player.is_aago_member else "NO") , player.name, rating, category, rated_games) for ranking, player, rating, category, rated_games in get_sorted_ratings()]
    lines.append("") # To get the last end of file character when joining
    return HttpResponse("\r\n".join(lines), content_type='text/plain')
    
