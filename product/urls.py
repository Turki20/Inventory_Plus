from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('all/', views.all_products_view, name='all_products_view'),
    path('add_product/', views.add_product_view, name='add_product_view'),
    path('update_product/<int:product_id>/', views.update_product_view, name='update_product_view'),
    path('deatil/<int:product_id>/', views.product_detail_view, name='product_detail_view'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    
    # category 
    path('all_category/', views.all_category_view, name="all_category_view"),
    path('add_category/', views.add_category_view, name='add_category_view'),
    path('update_categoty/<int:category_id>/', views.update_category_view, name='update_category_view'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
]
