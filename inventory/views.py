
from django.shortcuts import render
from .models import Product
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProductForm


def home(request):
    return render(request, "inventory/home.html")

@login_required
def dashboard(request):
    total_products = Product.objects.count()
    low_stock = Product.objects.filter(stock__lte=5).count()

    context = {
        "total_products": total_products,
        "low_stock": low_stock,
    }
    return render(request, "dashboard.html", context)


def product_list(request):
    products = Product.objects.all()
    return render(request, "inventory/product_list.html", {"products": products})

from django.shortcuts import render, redirect
from .models import Product

def add_product(request):
    if request.method == "POST":
        Product.objects.create(
            name=request.POST["name"],
            price=request.POST["price"],
            stock=request.POST["stock"]
        )
        return redirect("product_list")
    return render(request, "inventory/add_product.html")

def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect("product_list")
    return render(request, "inventory/edit_product.html", {"form": form})


def customer_list(request):
    return render(request, 'inventory/customer_list.html')

def supplier_list(request):
    return render(request, 'inventory/supplier_list.html')

def purchase_list(request):
    return render(request, 'inventory/purchase_list.html')

def sales_list(request):
    return render(request, 'inventory/sales_list.html')

# Reports
def purchase_report(request):
    return render(request, 'reports/purchase_report.html')

def sales_report(request):
    return render(request, 'reports/sales_report.html')

def stock_report(request):
    return render(request, 'reports/stock_report.html')


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect("product_list")
    return render(request, "inventory/delete_product.html", {"product": product})