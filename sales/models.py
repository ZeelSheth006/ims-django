from django.db import models
from inventory.models import Product

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_per_unit = models.FloatField()
    total_price = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
