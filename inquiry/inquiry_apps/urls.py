'''docstring'''
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views



app_name = 'inquiry_apps'

urlpatterns = [
    path('inquiry/login/', views.inquiry_login, name='inquiry_login'),
    path('inquiry/logout/', views.inquiry_logout, name='inquiry_logout'),
    path('inquiry/add/user/', views.user_add, name='user_add'),
    path('inquiry/add/user/success/', views.user_add_success, name='user_add_success'),
    path('inquiry/edit/profile/', views.edit_profile, name='edit_profile'),
    path('inquiry/edit/profile/avator/', views.edit_profile_avator, name='edit_profile_avator'),
    path('inquiry/edit/profile/username/', views.edit_profile_username, name='edit_profile_username'),
    path('inquiry/edit/profile/email/', views.edit_profile_email, name='edit_profile_email'),
    path('inquiry/edit/profile/password/', views.edit_profile_password, name='edit_password'),
    path('inquiry/edit/profile/success/', views.edit_profile_success, name='edit_profile_success'),
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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
