from django import forms
from .models import Product, Supplier, Customer

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "stock", "price"]



class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ["name", "email", "phone"]


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "email", "phone"]
