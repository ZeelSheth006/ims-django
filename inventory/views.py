from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm
from django.contrib import messages

def inventory_home(request):
    return render(request, "home.html")   # or create a template later



def product_list(request):
    products = Product.objects.all()
    return render(request, "inventory/product_list.html", {"products": products})


def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")
            return redirect("product_list")
    else:
        form = ProductForm()

    return render(request, "inventory/add_product.html", {"form": form})


def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect("product_list")
    else:
        form = ProductForm(instance=product)

    return render(request, "inventory/edit_product.html", {"form": form})


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, "Product deleted successfully!")
    return redirect("product_list")
