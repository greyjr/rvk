from django.shortcuts import render
from .models import Card


def index(request):
    return render(request, 'cards/main.html')


def personal_main(request, inn):
    context = Card.objects.get(inn)
    return render(request, 'cards/personal_main.html', context=context)
