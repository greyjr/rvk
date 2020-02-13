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
    phone = models.CharField(max_length=16, blank=True)
    work = models.CharField(max_length=256)
    vos = models.CharField(max_length=6)
    rank = models.CharField(max_length=24)
    vlk = models.DateField(blank=True)
    suitability = models.CharField(max_length=24)
    delay = models.DateField(blank=True)
    team = models.CharField(max_length=64)

    def age_person(self):
        yrs = {'1': 'рік', '234': 'роки', '567890': 'років'}
        age = date.today().year - self.birth_date.year
        yrs_str = next(v for k, v in yrs.items() if str(age % 10) in k)
        if age > 10 and str(age)[-2] == '1':
            yrs_str = 'років'
        return str(age) + ' ' + yrs_str

    def is_delay(self):
        return bool(self.delay)

    def is_vlk(self):
        return bool(self.vlk)

    def is_phone(self):
        return bool(self.phone)

    def fact_delay(self):
        if not self.is_delay:
            return ''
        if date.today() > self.delay:
            return 'минула'
        delta_days = date.today().day - self.delay.day
        delta_years = date.today().year - self.delay.year
        return '{} дн. ({} р.)'.format(str(delta_days), str(delta_years))

    def __str__(self):
        return self.surname_person + ' ' + self.name_person[0] + '. ' + self.patronymic_person[0] + '.'

    def get_first_personal_page_values(self):
        return [self.inn,
                self.surname_person,
                self.name_person,
                self.patronymic_person,
                self.birth_date,
                self.age_person(),
                self.phone,
                self.rank,
                self.suitability,
                self.delay]

    def get_second_personal_page_values(self):
        return [self.address_person,
                self.address_person_fact,
                self.work,
                self.vos,
                self.vlk,
                self.team]
