from django.shortcuts import render, redirect, get_object_or_404
from .models import Sale
from .forms import SaleForm
from inventory.models import Customer, Product,PurchaseBatch
from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib import messages


def sales_list(request):
    sales = Sale.objects.all().order_by("-created_at")
    return render(request, "sales/sales_list.html", {"sales": sales})

from django.shortcuts import render, redirect
from django.contrib import messages
from inventory.models import Product, PurchaseBatch
from .models import Sale


def add_sale(request):
    if request.method == "POST":
        product_id = request.POST.get("product")
        quantity = int(request.POST.get("quantity"))
        selling_price = float(request.POST.get("selling_price"))

        product = Product.objects.get(id=product_id)

        if product.stock < quantity:
            messages.error(request, "Not enough stock available")
            return redirect("add_sale")

        remaining_qty = quantity
        total_cost = 0

        # FIFO batches
        batches = PurchaseBatch.objects.filter(
            product=product, quantity_left__gt=0
        ).order_by("created_at")

        for batch in batches:
            if remaining_qty == 0:
                break

            used = min(batch.quantity_left, remaining_qty)
            total_cost += used * batch.price_per_unit

            batch.quantity_left -= used
            batch.save()

            remaining_qty -= used

        # Save Sale
        profit = (selling_price * quantity) - total_cost

        Sale.objects.create(
            product=product,
            quantity=quantity,
            selling_price=selling_price,
            cost_price=total_cost,
            profit=profit
        )

        # Update stock
        product.stock -= quantity
        product.save()

        messages.success(request, "Sale added successfully (FIFO applied)")
        return redirect("sale_list")

    products = Product.objects.all()
    return render(request, "sales/add_sale.html", {"products": products})


def edit_sale(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)

    if request.method == "POST":
        sale.quantity = int(request.POST["quantity"])
        sale.price = float(request.POST["price"])
        sale.save()
        return redirect("sales_list")

    return render(request, "sales/edit_sale.html", {"sale": sale})


def delete_sale(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    sale.delete()
    return redirect("sales_list")

def sale_invoice(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    return render(request, "sales/invoice_template.html", {"sale": sale})
