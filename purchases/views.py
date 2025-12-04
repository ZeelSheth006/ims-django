from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PurchaseForm
from inventory.models import Product


def add_purchase(request):
    if request.method == "POST":
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False)

            # Auto calculate total price
            quantity = form.cleaned_data['quantity']
            price_per_unit = form.cleaned_data['price_per_unit']
            purchase.total_price = quantity * price_per_unit

            purchase.save()

            # Update product stock
            product = purchase.product
            product.quantity += quantity
            product.save()

            messages.success(request, "Purchase added successfully!")
            return redirect("purchase_list")

    else:
        form = PurchaseForm()

    return render(request, "purchases/add_purchase.html", {"form": form})


def purchase_list(request):
    from .models import Purchase
    purchases = Purchase.objects.select_related("product").order_by("-date")
    return render(request, "purchases/purchase_list.html", {"purchases": purchases})
