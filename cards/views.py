from django.shortcuts import render
from .models import Card
from django.views.generic import View
from .forms import CardForm
from django.http import HttpResponseNotFound
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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


class CardEdit(View):
    def get(self, request, idi):
        old_data = Card.objects.get(id=idi).__dict__
        old_data.pop('_state')
        card_id = old_data.pop('id')
        form = CardForm(old_data)
        return render(request, 'cards/edit_card.html', context={'form': form, 'idi': card_id})

    def post(self, request, idi):
        bound_form = CardForm(request.POST)
        if bound_form.is_valid():
            bound_form.update(idi)
            return render(request, 'cards/main.html')
        return render(request, 'cards/edit_card.html', context={'form': bound_form, 'idi': idi})


def delete(request, idi):
    try:
        death_card = Card.objects.get(id=idi)
        death_card.delete()
    except Card.DoesNotExist:
        return HttpResponseNotFound('Картку не знайдено. Помилка.')
    return render(request, 'cards/main.html')


def base(request):
    card_list = Card.objects.all()
    paginator = Paginator(card_list, 3)
    page = request.GET.get('page')
    try:
        cards = paginator.page(page)
    except PageNotAnInteger:
        cards = paginator.page(1)
    except EmptyPage:
        cards = paginator.page(paginator.num_pages)
    return render(request, 'cards/base.html', context={'cards': cards})
