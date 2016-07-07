from django.shortcuts import render

from aago_ranking.ratings.models import PlayerRating


def homepage(request):
    ratings = PlayerRating.objects.order_by('event').select_related('player')
    last_ratings = {r.player: r.mu for r in ratings}
    sorted_ratings = sorted(last_ratings.items(), reverse=True, key=(lambda item: item[1]))
    return render(request, 'pages/home.html', {'sorted_ratings': sorted_ratings, })
