from django.shortcuts import render
from .models import Card
from django.views.generic import View
from .forms import CardForm


def index(request):
    return render(request, 'cards/main.html')


def personal_main(request, inn):
    context = Card.objects.get(inn)
    return render(request, 'cards/personal_main.html', context=context)


class CardCreate(View):
    def get(self, request):
        form = CardForm()
        return render(request, 'cards/create_card.html', context={'form': form})

    def post(self, request):
        bound_form = CardForm(request.POST)
        if bound_form.is_valid():
            bound_form.save()
            return render(request, 'cards/main.html')       # F I X
        return render(request, 'cards/create_card.html', context={'form': bound_form})
