from django import forms
from .models import Card
from django.contrib.admin.widgets import AdminDateWidget
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

suitability_variants = ('придатний', 'обмежено придатний', 'непридатний')
rank_variants = ('мол. лейтенант', 'лейтенант', 'ст. лейтенант', 'капітан', 'підполковник', 'полковник')


def validate_inn_length(inn_raw):
    if len(str(inn_raw)) != 10:
        raise ValidationError('Потрібно 10 цифр')


def validate_inn_unique(inn_raw):
    try:
        Card.objects.get(inn=inn_raw)
    except Card.DoesNotExist:
        pass
    else:
        raise ValidationError('такий номер існує !')


class CardForm(forms.Form):
    inn = forms.DecimalField(decimal_places=0,
                             validators=[validate_inn_length, validate_inn_unique],
                             label='Персональний номер')
    surname_person = forms.CharField(max_length=64, label='Прізвіще')
    name_person = forms.CharField(max_length=64, label="Ім'я")
    patronymic_person = forms.CharField(max_length=64, label='По-батькові')
    birth_date = forms.DateField(label='Дата народження')
    address_person = forms.CharField(max_length=128, label='Адреса реєстрації')
    address_person_fact = forms.CharField(max_length=128, label='Проживає', required=False)
    # phone = forms.DecimalField(max_digits=9, decimal_places=0, label='Телефон', required=False)  # (+380 ...)
    phone = forms.CharField(validators=[
        RegexValidator(regex='^((8|\+38)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', message="Wrong number")],
        required=False)
    work = forms.CharField(max_length=256, label='Місце роботи/посада', initial='ТНП')
    vos = forms.CharField(max_length=6, label='ВОС')
    rank = forms.ChoiceField(label='Звання', choices=tuple((x, x) for x in rank_variants))
    vlk = forms.DateField(widget=AdminDateWidget, label='ВЛК', required=False)
    suitability = forms.ChoiceField(label='Придатність', choices=tuple((x, x) for x in suitability_variants))
    delay = forms.DateField(label='Відсрочка', required=False)
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
        if not self.cleaned_data['address_person_fact']:
            self.cleaned_data['address_person_fact'] = self.cleaned_data['address_person']
        self.cleaned_data['phone'].replace(' ', '')
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


class CardFormEdit(CardForm):
    inn = forms.DecimalField(label='Персональний номер')
    inn.widget.attrs.update({'readonly': 'readonly', 'class': 'form-control form-control-sm'})

    def update(self, idi):
        re_card = Card.objects.get(id=idi)
        re_card.surname_person = self.cleaned_data['surname_person']
        re_card.name_person = self.cleaned_data['name_person']
        re_card.patronymic_person = self.cleaned_data['patronymic_person']
        re_card.birth_date = self.cleaned_data['birth_date']
        re_card.address_person = self.cleaned_data['address_person']
        re_card.address_person_fact = self.cleaned_data['address_person_fact']
        re_card.phone = self.cleaned_data['phone'].replace(' ', '')
        re_card.work = self.cleaned_data['work']
        re_card.vos = self.cleaned_data['vos']
        re_card.rank = self.cleaned_data['rank']
        re_card.vlk = self.cleaned_data['vlk']
        re_card.suitability = self.cleaned_data['suitability']
        re_card.delay = self.cleaned_data['delay']
        re_card.team = self.cleaned_data['team']
        re_card.save()
        return re_card
