from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from django.shortcuts import render
from inventory.models import Product
from purchases.models import Purchase
from sales.models import Sale


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully! Please login.")

            # Redirect with username pre-filled
            return redirect(f"/accounts/login/?u={user.username}")
    else:
        form = SignupForm()

    return render(request, "accounts/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect("dashboard")   # ✅ Redirect instantly
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")




def logout_view(request):
    logout(request)
    return redirect("login")









@login_required
def dashboard(request):
    # --- KPI Metrics ---
    total_products = Product.objects.count()
    total_stock_quantity = (
        Product.objects.aggregate(total_qty=Sum("quantity"))["total_qty"] or 0
    )

    total_purchase_value = (
        Purchase.objects.aggregate(total=Sum("total_price"))["total"] or 0
    )
    total_sales_value = (
        Sale.objects.aggregate(total=Sum("total_price"))["total"] or 0
    )

    net_profit = total_sales_value - total_purchase_value

    # --- Last 7 days chart data (Purchases vs Sales) ---
    today = now().date()
    labels = []
    purchase_data = []
    sales_data = []

    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        labels.append(day.strftime("%d-%b"))  # e.g., 02-Dec

        day_purchases = (
            Purchase.objects.filter(date=day)
            .aggregate(total=Sum("total_price"))["total"]
            or 0
        )
        day_sales = (
            Sale.objects.filter(date=day)
            .aggregate(total=Sum("total_price"))["total"]
            or 0
        )

        purchase_data.append(float(day_purchases))
        sales_data.append(float(day_sales))

    context = {
        "total_products": total_products,
        "total_stock_quantity": total_stock_quantity,
        "total_purchase_value": total_purchase_value,
        "total_sales_value": total_sales_value,
        "net_profit": net_profit,
        "labels": labels,
        "purchase_data": purchase_data,
        "sales_data": sales_data,
    }

    return render(request, "accounts/dashboard.html", context)
