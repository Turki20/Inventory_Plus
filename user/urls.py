from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('all_users/', views.all_users, name='all_users_view'),
    path('add_user/', views.add_user_view, name='add_user_view'),
    path('update_user/<int:user_id>/', views.update_user_view, name='update_user_view'),
]
