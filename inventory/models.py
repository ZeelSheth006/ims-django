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
    name = models.CharField(max_length=100)
    price = models.FloatField()
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name



class PurchaseBatch(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_left = models.IntegerField()
    price_per_unit = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} | {self.quantity_left}"
