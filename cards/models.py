from django.db import models
# from django.forms import MultiWidget, TextInput
from datetime import date


# class PhoneWidget(MultiWidget):
#     def __init__(self, code_length=3, num_length=7, attrs=None):
#         widgets = [TextInput(attrs={'size': code_length, 'maxlength': code_length}),
#                    TextInput(attrs={'size': num_length, 'maxlength': num_length})]
#         super(PhoneWidget, self).__init__(widgets, attrs)
#
#     def decompress(self, value):
#         if value:
#             return [value.code, value.number]
#         else:
#             return ['', '']
#
#     def phone_output(self, rendered_widgets):
#         return '+38' + '(' + rendered_widgets[0] + ') - ' + rendered_widgets[1]


class Card(models.Model):
    inn = models.DecimalField(max_digits=10, decimal_places=0)
    surname_person = models.CharField(max_length=64)
    name_person = models.CharField(max_length=64)
    patronymic_person = models.CharField(max_length=64)
    birth_date = models.DateField()
    address_person = models.CharField(max_length=128)
    address_person_fact = models.CharField(max_length=128)
    phone = models.CharField(max_length=16, blank=True, null=True)
    work = models.CharField(max_length=256)
    vos = models.CharField(max_length=6)
    rank = models.CharField(max_length=24)
    vlk = models.DateField(blank=True, null=True)
    suitability = models.CharField(max_length=24)
    delay = models.DateField(blank=True, null=True)
    team = models.CharField(max_length=64)

    def __str__(self):
        return self.surname_person + ' ' + self.name_person[0] + '. ' + self.patronymic_person[0] + '.'

    def age_person(self):
        yrs = {'1': 'рік', '234': 'роки', '567890': 'років'}
        age = date.today().year - self.birth_date.year
        yrs_str = next(v for k, v in yrs.items() if str(age % 10) in k)
        if age > 10 and str(age)[-2] == '1':
            yrs_str = 'років'
        return str(age) + ' ' + yrs_str

    def get_phone(self):
        if self.phone:
            raw_number = self.phone[::-1]
            number_to_template = raw_number[:2] + ' ' + raw_number[2:4] + ' ' + raw_number[4:7] + ' ' + raw_number[7:]
            return number_to_template[::-1]
        else:
            return 'Не вказаний'

    def get_vlk(self):
        if self.vlk:
            return self.vlk
        else:
            return 'Не вказана'

    def get_delay(self):
        if self.delay:
            return self.delay
        else:
            return 'Немає'

    def fact_delay(self):
        if not self.delay:
            return ''
        if date.today() > self.delay:
            return 'закінчилась'
        delta_days = self.delay.day - date.today().day
        delta_month = self.delay.month - date.today().month
        delta_years = self.delay.year - date.today().year
        return '{} р. {} міс. {} дн.'.format(str(delta_years), str(delta_month), str(delta_days))

    def get_pib(self):
        return self.surname_person + ' ' + self.name_person + ' ' + self.patronymic_person

    def get_left_card(self):
        return {'Персональний номер': self.inn,
                "Дата народження": self.birth_date,
                "Вік": self.age_person(),
                "Телефон": self.get_phone(),
                "Звання": self.rank,
                "Придатність": self.suitability,
                "Відсрочка": self.get_delay(),
                "": self.fact_delay()}

    def get_right_card(self):
        return {"Адреса реєстрації": self.address_person,
                "Фактична адреса проживання": self.address_person_fact,
                "Місце роботи / посада": self.work,
                "ВОС": self.vos,
                "ВЛК": self.get_vlk(),
                "Команда": self.team}

    def delay_color(self):
        if self.delay < date.today():
            color = '#2cb864'
        else:
            color = '#da0560'
        return color
