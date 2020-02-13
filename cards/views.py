from django.shortcuts import render, redirect
from .models import Card
from django.views.generic import View
from .forms import CardForm, CardFormEdit
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
            return redirect('base_url')
        return render(request, 'cards/create_card.html', context={'form': bound_form})


class CardEdit(View):
    def get(self, request, idi):
        old_data = Card.objects.get(id=idi).__dict__
        old_data.pop('_state')
        card_id = old_data.pop('id')
        form = CardFormEdit(old_data)
        return render(request, 'cards/edit_card.html', context={'form': form, 'idi': card_id})

    def post(self, request, idi):
        bound_form = CardFormEdit(request.POST)
        if bound_form.is_valid():
            bound_form.update(idi)
            return redirect('base_url')
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
    card_list = Card.objects.all().order_by(mode)
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
                    "Вік",
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
    data_first = {fields_first[i]: card.get_first_personal_page_values()[i] for i in range(10)}
    data_second = {fields_second[i]: card.get_second_personal_page_values()[i] for i in range(6)}
    return render(request, 'cards/personal_main.html', context={'data_first': data_first,
                                                                'data_second': data_second,
                                                                'idi': idi})


def parsed(line):
    numbers = []
    line_split = line.replace(',', ' ').replace('.', ' ').split(' ')
    for position in range(len(line_split)):
        may_be = ''
        for i in line_split[position]:
            if i in '0123456789':
                may_be += i
        if len(may_be) in range(3, 7):
            numbers.append(may_be)
    return numbers


def search(request, field):
    if field not in ['inn', 'rank', 'vos', 'surname_person']:
        return render(request, 'cards/main.html')
    line = request.GET.get('line')
    if not line:
        return redirect('base_url')
    if field == 'vos':
        numbers = parsed(line)
        data = Card.objects.filter(vos__contains=numbers[0])
        for number in numbers[1:]:
            data = data.union(Card.objects.filter(vos__contains=number))
    elif field == 'rank':
        data = Card.objects.filter(rank__exact=line)
    else:
        data = Card.objects.filter(**{'{}'.format(field): line})
    return render(request, 'cards/result.html', context={'cards': data})
