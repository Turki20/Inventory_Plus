from django.urls import path
from . import views

app_name = 'supplier'

urlpatterns = [
    path('all_supplier', views.all_suppliers_view, name='all_suppliers_view'),
    path('add_supplier', views.add_supplier_view, name='add_supplier_view'),
    path('update_supplier/<int:supplier_id>/', views.update_supplier_view, name='update_supplier_view'),
    path('delete_supplier/<int:supplier_id>/', views.delete_supplier, name='delete_supplier'),
]
