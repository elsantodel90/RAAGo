from django.shortcuts import render
from django.http import HttpResponse

from aago_ranking.ratings.models import PlayerRating

import datetime

def ratingIsValid(r):
    # We do not care about leap years at all for these purposes
    anYearAgo = datetime.date.today() - datetime.timedelta(days=365)
    return r.player.is_aago_member or anYearAgo < r.event.end_date

def get_sorted_ratings():
    ratings = PlayerRating.objects.order_by('event')
    # Note: this query retrieves *every* rating from the DB.
    #   It can be optimized if needed.
    last_ratings = {r.player: r.mu for r in ratings if ratingIsValid(r)}
    return sorted(last_ratings.items(), reverse=True, key=(lambda item: item[1]))

def homepage(request):
    return render(request, 'pages/home.html', {'sorted_ratings': get_sorted_ratings(), })

def csv_ranking(request):
    lines = ["Ranking;Jugador;Rating"]
    lines += ["{};{};{:.3}".format(i+1, player.name, rating) for i, (player, rating) in enumerate(get_sorted_ratings())]
    lines.append("") # To get the last end of file character when joining
    return HttpResponse("\r\n".join(lines), content_type='text/plain')
    
