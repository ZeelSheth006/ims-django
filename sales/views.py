from django.shortcuts import render, redirect
from django.contrib import messages
from inventory.models import Product
from .models import Sale
from purchases.models import Purchase
from .forms import SaleForm
from .models import Sale


def sale_list(request):
    sales = Sale.objects.all().order_by("-id")
    return render(request, "sales/sale_list.html", {"sales": sales})


def add_sale(request):
    if request.method == "POST":
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            product = sale.product

            # Check stock
            if sale.quantity > product.quantity:
                messages.error(request, "Not enough stock available!")
                return redirect("add_sale")

            # FIFO stock deduction
            needed_qty = sale.quantity
            batches = Purchase.objects.filter(product=product).order_by("date")

            for batch in batches:
                if needed_qty <= 0:
                    break

                if batch.quantity >= needed_qty:
                    batch.quantity -= needed_qty
                    batch.save()
                    needed_qty = 0
                else:
                    needed_qty -= batch.quantity
                    batch.quantity = 0
                    batch.save()

            # Update product stock
            product.quantity -= sale.quantity
            product.save()

            # Save sale record
            sale.total_price = sale.quantity * sale.price_per_unit
            sale.save()

            messages.success(request, "Sale recorded successfully!")
            return redirect("sale_list")

    else:
        form = SaleForm()

    return render(request, "sales/add_sale.html", {"form": form})


def sales_home(request):
    return render(request, "sales/sales_home.html")



def add_sale(request):
    if request.method == "POST":
        product_id = request.POST.get("product")
        quantity = int(request.POST.get("quantity"))
        price = float(request.POST.get("sale_price"))

        product = Product.objects.get(id=product_id)

        if product.stock < quantity:
            messages.error(request, "Not enough stock!")
            return redirect("add_sale")

        product.stock -= quantity
        product.save()

        Sale.objects.create(product=product, quantity=quantity, sale_price=price)

        messages.success(request, "Sale recorded successfully!")
        return redirect("add_sale")

    products = Product.objects.all()
    return render(request, "sales/add_sale.html", {"products": products})

def sales_home(request):
    return render(request, "sales/home.html")
