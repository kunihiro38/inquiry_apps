from django.urls import path
from . import views

app_name = 'inquiry_apps'

urlpatterns = [
    path('', views.index, name='index'),
    path('inquiry/add/', views.inquiry_add, name='inquiry_add'),
    path('inquiry/add/success/', views.inquiry_add_success, name='inquiry_add_success'),
    path('inquiry/list/', views.inquiry_list, name='inquiry_list'),
    path('inquiry/<int:inquiry_id>/comment/list/', views.comment_list, name='comment_list'),
    path('inquiry/<int:inquiry_id>/comment/add/', views.comment_add, name='comment_add'),
    path('inquiry/<int:inquiry_id>/comment/add/success/', views.comment_add_success, name='comment_add_success'),
    # path('inquiry/<int:inquiry_id>/comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete')
    # path('inquiry/<int:inquiry_id>/comment/<int:comment_id>/delete/success/', views.comment_delete_success, name='comment_delete_success')

]