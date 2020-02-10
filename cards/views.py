from django.shortcuts import render, redirect
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
            return redirect('base_url')
            # return render(request, 'cards/main.html')
        return render(request, 'cards/edit_card.html', context={'form': bound_form, 'idi': idi})


def delete(request, idi):
    try:
        death_card = Card.objects.get(id=idi)
        death_card.delete()
    except Card.DoesNotExist:
        return HttpResponseNotFound('Картку не знайдено. Помилка.')
    return render(request, 'cards/main.html')


def base(request):
    mode = request.GET.get('mode')
    if mode not in ['inn', 'surname_person', 'rank', 'vos']:
        mode = 'surname_person'
    card_list_unsort = Card.objects.all()
    card_list = card_list_unsort.order_by(mode)
    paginator = Paginator(card_list, 25, orphans=3)
    page = request.GET.get('page')
    try:
        cards = paginator.page(page)
    except PageNotAnInteger:
        cards = paginator.page(1)
    except EmptyPage:
        cards = paginator.page(paginator.num_pages)
    return render(request, 'cards/base.html', context={'cards': cards, 'mode': mode})


def personal_view(request, idi):
    card = Card.objects.get(id=idi)
    fields_first = ['Персональний номер',
                    "Прізвище",
                    "Ім'я",
                    'По-батькові',
                    "Дата народження",
                    "Телефон",
                    "Звання",
                    "Придатність",
                    "Відсрочка"]
    fields_second = ["Адреса реєстрації",
                     "Фактична адреса проживання",
                     "Місце роботи / посада",
                     "ВОС",
                     "ВЛК",
                     "Команда"]
    data_first = {fields_first[i]: card.get_first_personal_page_values()[i] for i in range(9)}
    data_second = {fields_second[i]: card.get_second_personal_page_values()[i] for i in range(6)}
    return render(request, 'cards/personal_main.html', context={'data_first': data_first,
                                                                'data_second': data_second,
                                                                'idi': idi})
