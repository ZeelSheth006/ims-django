from django.shortcuts import render, redirect
from inventory.models import Purchase, Sale, Product
from django.contrib import messages
from django.db import transaction

@transaction.atomic
def add_sale(request):
    if request.method == "POST":
        product_id = request.POST.get("product")
        quantity = float(request.POST.get("quantity"))
        sale_price = float(request.POST.get("sale_price"))

        product = Product.objects.get(id=product_id)

        # 1️⃣ Get all purchase batches with remaining stock
        purchase_batches = Purchase.objects.filter(
            product=product, remaining_qty__gt=0
        ).order_by("purchase_date")  # FIFO

        qty_needed = quantity

        for batch in purchase_batches:
            if qty_needed <= 0:
                break

            available = float(batch.remaining_qty)

            if available >= qty_needed:
                batch.remaining_qty = available - qty_needed
                batch.save()
                qty_needed = 0
            else:
                qty_needed -= available
                batch.remaining_qty = 0
                batch.save()

        if qty_needed > 0:
            messages.error(request, "Not enough stock for this sale.")
            return redirect("add_sale")

        # 2️⃣ Create the sale record
        Sale.objects.create(
            product=product,
            quantity=quantity,
            sale_price=sale_price
        )

        messages.success(request, "Sale added successfully.")
        return redirect("sales_list")

    products = Product.objects.all()
    return render(request, "sales/add_sale.html", {"products": products})
