from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    url(r'^$', views.index),
    # path('personal_main/<int:inn>', views.personal_main),
]