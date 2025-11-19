from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=150, blank=True, null=True)
    unit = models.CharField(max_length=50, default="pcs")  # kg, litre, pcs, etc.
    minimum_stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    purchase_date = models.DateField(auto_now_add=True)

    # FIFO Tracking: remaining quantity from this batch
    remaining_qty = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.total_cost = self.quantity * self.price_per_unit
            self.remaining_qty = self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} purchased"


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_sale = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    sale_date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.total_sale = self.quantity * self.sale_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} sold"
