from django.urls import path
from . import views

app_name = 'inquiry_apps'

urlpatterns = [
    path('', views.index, name='index'),
]