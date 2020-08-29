from django.urls import path
from . import views

app_name = 'inquiry_apps'

urlpatterns = [
    path('inquiry/login/', views.inquiry_login, name='inquiry_login'),
    path('inquiry/logout/', views.inquiry_logout, name='inquiry_logout'),
    path('inquiry/add/user/', views.user_add, name='user_add'),
    path('inquiry/edit/profile/', views.edit_profile, name='edit_profile'),
    path('inquiry/edit/profile/name/', views.edit_name, name='edit_name'),
    path('inquiry/edit/profile/email/', views.edit_email, name='edit_email'),
    path('inquiry/edit/profile/password/', views.edit_password, name='edit_password'),
    path('', views.index, name='index'),
    path('inquiry/add/', views.inquiry_add, name='inquiry_add'),
    path('inquiry/add/success/', views.inquiry_add_success, name='inquiry_add_success'),
    path('inquiry/list/', views.inquiry_list, name='inquiry_list'),
    path('inquiry/list/ajax/', views.inquiry_list_ajax, name='inquiry_list_ajax'),
    path('inquiry/list/ajax/response/', views.inquiry_list_ajax_response, name='inquiry_list_ajax_response'),
    path('inquiry/<int:inquiry_id>/comment/list/', views.comment_list, name='comment_list'),
    path('inquiry/<int:inquiry_id>/comment/add/', views.comment_add, name='comment_add'),
    path('inquiry/<int:inquiry_id>/comment/add/success/', views.comment_add_success, name='comment_add_success'),
    path('inquiry/<int:inquiry_id>/comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('inquiry/<int:inquiry_id>/comment/delete/success/', views.delete_comment_success, name='delete_comment_success'),
    path('inquiry/<int:inquiry_id>/comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('inquiry/<int:inquiry_id>/comment/<int:comment_id>/edit/success/', views.edit_comment_success, name='edit_comment_success'),
]