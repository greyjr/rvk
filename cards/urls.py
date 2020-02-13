from django.conf.urls import url
from django.urls import path
from .views import *


urlpatterns = [
    url(r'^$', index, name='main_url'),
    path('create', CardCreate.as_view(), name='card_create_url'),
    path('edit/<int:idi>', CardEdit.as_view(), name='card_edit_url'),
    path('delete/<int:idi>', delete, name='card_delete_url'),
    path('base', base, name='base_url'),
    path('personal_view/<int:idi>', personal_view, name='personal_view_url'),
    path('search/<str:field>', search, name='search_url'),
]
