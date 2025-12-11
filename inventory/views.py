from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Supplier, Customer
from .models import Product, Supplier, Customer, Category


# -------------------- DASHBOARD --------------------
@login_required
def dashboard(request):
    context = {
        "total_products": Product.objects.count(),
        "total_suppliers": Supplier.objects.count(),
        "total_customers": Customer.objects.count(),
        "low_stock_products": Product.objects.filter(stock__lt=5),
    }
    return render(request, "dashboard.html", context)


# -------------------- PRODUCT CRUD --------------------
@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, "inventory/product_list.html", {"products": products})


@login_required
def product_create(request):
    categories = Category.objects.all()
    suppliers = Supplier.objects.all()

    if request.method == "POST":
        name = request.POST["name"]
        category_id = request.POST["category"]
        stock = request.POST["stock"]
        price = request.POST["price"]
        supplier_id = request.POST.get("supplier")

        category = Category.objects.get(id=category_id)
        supplier = Supplier.objects.get(id=supplier_id) if supplier_id else None

        Product.objects.create(
            name=name,
            category=category,
            stock=stock,
            price_per_unit=price,
            supplier=supplier,
        )
        return redirect("product_list")

    return render(
        request,
        "inventory/product_form.html",
        {"categories": categories, "suppliers": suppliers},
    )


@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    categories = Category.objects.all()
    suppliers = Supplier.objects.all()

    if request.method == "POST":
        product.name = request.POST["name"]
        product.category = Category.objects.get(id=request.POST["category"])
        product.stock = request.POST["stock"]
        product.price_per_unit = request.POST["price"]
        supplier_id = request.POST.get("supplier")
        product.supplier = Supplier.objects.get(id=supplier_id) if supplier_id else None
        product.save()
        return redirect("product_list")

    return render(
        request,
        "inventory/product_form.html",
        {"product": product, "categories": categories, "suppliers": suppliers},
    )


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect("product_list")
    return render(request, "inventory/product_confirm_delete.html", {"product": product})


# -------------------- SUPPLIER CRUD --------------------
@login_required
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, "inventory/supplier_list.html", {"suppliers": suppliers})


@login_required
def supplier_create(request):
    if request.method == "POST":
        Supplier.objects.create(
            name=request.POST["name"],
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            address=request.POST.get("address"),
        )
        return redirect("supplier_list")

    return render(request, "inventory/supplier_form.html")


@login_required
def supplier_edit(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)

    if request.method == "POST":
        supplier.name = request.POST["name"]
        supplier.email = request.POST.get("email")
        supplier.phone = request.POST.get("phone")
        supplier.address = request.POST.get("address")
        supplier.save()
        return redirect("supplier_list")

    return render(request, "inventory/supplier_form.html", {"supplier": supplier})


@login_required
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == "POST":
        supplier.delete()
        return redirect("supplier_list")
    return render(request, "inventory/supplier_confirm_delete.html", {"supplier": supplier})


# -------------------- CUSTOMER CRUD --------------------
@login_required
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, "inventory/customer_list.html", {"customers": customers})


@login_required
def customer_create(request):
    if request.method == "POST":
        Customer.objects.create(
            name=request.POST["name"],
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            address=request.POST.get("address"),
        )
        return redirect("customer_list")

    return render(request, "inventory/customer_form.html")


@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == "POST":
        customer.name = request.POST["name"]
        customer.email = request.POST.get("email")
        customer.phone = request.POST.get("phone")
        customer.address = request.POST.get("address")
        customer.save()
        return redirect("customer_list")

    return render(request, "inventory/customer_form.html", {"customer": customer})


@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        customer.delete()
        return redirect("customer_list")
    return render(request, "inventory/customer_confirm_delete.html", {"customer": customer})
