from django.db import models

# ==========================
#        CATEGORY
# ==========================
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# ==========================
#        SUPPLIER
# ==========================
class Supplier(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# ==========================
#        CUSTOMER
# ==========================
class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# ==========================
#        PRODUCT
# ==========================
class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    stock = models.IntegerField(default=0)
    price = models.FloatField(default=0.0)

    def __str__(self):
        return self.name
