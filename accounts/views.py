from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
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






def dashboard(request):
    total_products = Product.objects.count()
    total_purchases = Purchase.objects.count()
    total_sales = Sale.objects.count()

    context = {
        "total_products": total_products,
        "total_purchases": total_purchases,
        "total_sales": total_sales,
    }

    return render(request, "accounts/dashboard.html", context)

def dashboard(request):
    context = {
        "product_count": Product.objects.count(),
        "purchase_count": Purchase.objects.count(),
        "sale_count": Sale.objects.count(),
    }
    return render(request, "dashboard.html", context)



