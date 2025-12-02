from django.shortcuts import render, redirect
from .forms import PurchaseForm
from .models import Purchase
from inventory.models import Product
from django.contrib import messages

def purchase_list(request):
    purchases = Purchase.objects.all().order_by("-id")
    return render(request, "purchases/purchase_list.html", {"purchases": purchases})


def add_purchase(request):
    if request.method == "POST":
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.total_price = purchase.quantity * purchase.price_per_unit
            purchase.save()

            # Update Stock
            product = purchase.product
            product.quantity += purchase.quantity
            product.save()

            messages.success(request, "Purchase added & stock updated!")
            return redirect("purchase_list")

    else:
        form = PurchaseForm()

    return render(request, "purchases/add_purchase.html", {"form": form})
