from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('sign_in/', views.sign_in_view, name='sign_in_view'),
    path('sign_out/', views.log_out, name='log_out'),
]
