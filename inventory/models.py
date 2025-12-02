from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, blank=True)
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0)

    def __str__(self):
        return self.name
quantity = models.IntegerField(default=0)
