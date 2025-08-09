from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('all/', views.all_products_view, name='all_products_view'),
    path('add_product/', views.add_product_view, name='add_product_view'),
    path('update_product/<int:product_id>/', views.update_product_view, name='update_product_view'),
    path('deatil/<int:product_id>/', views.product_detail_view, name='product_detail_view'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
]
