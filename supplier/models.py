from django.db import models

# Create your models here.

class Supplier(models.Model):
    name = models.CharField(max_length=255) # uniqu
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
