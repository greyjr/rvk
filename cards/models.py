from django.db import models
from django.forms import MultiWidget, TextInput


class PhoneWidget(MultiWidget):
    def __init__(self, code_length=3, num_length=7, attrs=None):
        widgets = [TextInput(attrs={'size': code_length, 'maxlength': code_length}),
                   TextInput(attrs={'size': num_length, 'maxlength': num_length})]
        super(PhoneWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.code, value.number]
        else:
            return ['', '']

    def phone_output(self, rendered_widgets):
        return '+38' + '(' + rendered_widgets[0] + ') - ' + rendered_widgets[1]


class Card(models.Model):
    inn = models.DecimalField(max_digits=10, decimal_places=0)
    surname_person = models.CharField(max_length=64)
    name_person = models.CharField(max_length=64)
    patronymic_person = models.CharField(max_length=64)
    birth_date = models.DateField()
    address_person = models.CharField(max_length=128)
    address_person_fact = models.CharField(max_length=128)
    phone = PhoneWidget()
    work = models.CharField(max_length=256, default='ТНП')
    vos = models.CharField(max_length=6)
    suitability = models.CharField(max_length=24)
    delay = models.DateField()
    team = models.CharField(max_length=64, default='без команди')
