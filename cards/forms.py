from django import forms
from .models import Card
from django.contrib.admin.widgets import AdminDateWidget

suitability_variants = ('придатний', 'обмежено придатний', 'непридатний')
rank_variants = ('мол. лейтенант', 'лейтенант', 'ст. лейтенант', 'капітан', 'підполковник', 'полковник')


class CardForm(forms.Form):
    inn = forms.DecimalField(max_digits=10, decimal_places=0, label='Персональний номер')
    surname_person = forms.CharField(max_length=64, label='Прізвіще')
    name_person = forms.CharField(max_length=64, label="Ім'я")
    patronymic_person = forms.CharField(max_length=64, label='По-батькові')
    birth_date = forms.DateField(label='Дата народження')
    address_person = forms.CharField(max_length=128, label='Адреса реєстрації')
    address_person_fact = forms.CharField(max_length=128, label='Проживає')
    phone = forms.DecimalField(max_digits=9, decimal_places=0, label='Телефон', help_text='+380')  # (+380 ...)
    work = forms.CharField(max_length=256, label='Місце роботи/посада', initial='ТНП')
    vos = forms.CharField(max_length=6, label='ВОС')
    rank = forms.ChoiceField(label='Звання', choices=tuple((x, x) for x in rank_variants))
    vlk = forms.DateField(widget=AdminDateWidget, label='ВЛК')
    suitability = forms.ChoiceField(label='Придатність', choices=tuple((x, x) for x in suitability_variants))
    delay = forms.DateField(label='Відсрочка')
    team = forms.CharField(max_length=64, label='Команда', initial='без команди')

    inn.widget.attrs.update({'class': 'form-control form-control-sm'})
    surname_person.widget.attrs.update({'class': 'form-control form-control-sm'})
    name_person.widget.attrs.update({'class': 'form-control form-control-sm'})
    patronymic_person.widget.attrs.update({'class': 'form-control form-control-sm'})
    birth_date.widget.attrs.update({'class': 'form-control form-control-sm'})
    address_person.widget.attrs.update({'class': 'form-control form-control-sm'})
    address_person_fact.widget.attrs.update({'class': 'form-control form-control-sm'})
    phone.widget.attrs.update({'class': 'form-control form-control-sm'})
    work.widget.attrs.update({'class': 'form-control form-control-sm'})
    vos.widget.attrs.update({'class': 'form-control form-control-sm'})
    rank.widget.attrs.update({'class': 'form-control form-control-sm'})
    vlk.widget.attrs.update({'class': 'form-control form-control-sm'})
    suitability.widget.attrs.update({'class': 'form-control form-control-sm'})
    delay.widget.attrs.update({'class': 'form-control form-control-sm'})
    team.widget.attrs.update({'class': 'form-control form-control-sm'})

    def save(self):
        new_card = Card.objects.create(
            inn=self.cleaned_data['inn'],
            surname_person=self.cleaned_data['surname_person'],
            name_person=self.cleaned_data['name_person'],
            patronymic_person=self.cleaned_data['patronymic_person'],
            birth_date=self.cleaned_data['birth_date'],
            address_person=self.cleaned_data['address_person'],
            address_person_fact=self.cleaned_data['address_person_fact'],
            phone=self.cleaned_data['phone'],
            work=self.cleaned_data['work'],
            vos=self.cleaned_data['vos'],
            rank=self.cleaned_data['rank'],
            vlk=self.cleaned_data['vlk'],
            suitability=self.cleaned_data['suitability'],
            delay=self.cleaned_data['delay'],
            team=self.cleaned_data['team']
        )
        return new_card
