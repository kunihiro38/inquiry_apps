from django.urls import path
from . import views

app_name = 'inquiry_apps'

urlpatterns = [
    path('', views.index, name='index'),
    path('inquiry/add/', views.inquiry_add, name='inquiry_add'),
    # path('inquirys/add_success/', views.inquiry_add_success, name='inquiry_add_success'),
    path('inquiry/list/', views.inquiry_list, name='inquiry_list'),
    
]