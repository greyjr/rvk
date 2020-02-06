from django.conf.urls import url
from django.urls import path
from .views import *


urlpatterns = [
    url(r'^$', index),
    path('create', CardCreate.as_view(), name='card_create_url'),
]