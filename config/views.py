from django.shortcuts import render
from django.http import HttpResponse

from aago_ranking.ratings.models import PlayerRating

def homepage(request):
    # TemplateView.as_view(template_name='pages/home.html')
    allHistoryRatings = PlayerRating.objects.order_by('event')
    playerRatings = dict()
    for rating in allHistoryRatings:
        playerRatings[rating.player.name] = rating.mu
    sortedRatings = sorted(playerRatings.items(), reverse=True, key=(lambda item : item[1]))
    players = [{"ranking" : i+1, "rating" : "{:.3f}".format(mu), "name" : name} for i, (name, mu) in enumerate(sortedRatings)]
    return render(request, 'pages/home.html', {
        'players': players, #[{ "ranking" : 1, "rating" : 1.521, "name" : "Rodrigo Batata" }, ],
    })

