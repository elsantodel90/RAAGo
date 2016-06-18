from django.shortcuts import render
from django.http import HttpResponse


def test(request):
    name = request.GET.get('name')
    return render(request, 'games/test.html', {
        'name': name,
        'values': [1, 2, 3, 4, 5],
    })


def test_2(request, name):
    return render(request, 'games/test.html', {
        'name': name,
        'values': [1, 2, 3, 4, 5],
    })
