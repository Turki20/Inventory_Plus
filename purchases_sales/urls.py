from django.urls import path
from . import views


app_name = 'purchases_sales'

urlpatterns = [
    path('', views.purchases_sales_view, name='purchases_sales_view'),
    path('add_purchase/', views.add_purchase_view, name='add_purchase_view'),
    path('add_sale/', views.add_sale_view, name='add_sale_view'),
    path('delete_sale/<int:sale_id>/', views.delete_sale, name='delete_sale'),
    path('delete_purchase/<int:purchase_id>/', views.delete_purchase, name='delete_purchase'),
]
