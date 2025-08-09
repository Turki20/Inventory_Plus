from django.db import models
from supplier.models import Supplier



# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True) 
    image = models.ImageField(upload_to='images/', default='images/product_image.png')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True) # many to many
    description = models.TextField(blank=True)
    
    quantity_in_stock = models.PositiveIntegerField(default=0)
    min_quantity_alert = models.PositiveIntegerField(default=5)  # للتنبيه عند الانخفاض
    
    cost_price = models.FloatField()
    selling_price = models.FloatField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
