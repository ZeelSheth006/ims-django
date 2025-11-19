from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone

from .forms import SignupForm


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect("login")
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

            # Save session data
            request.session["last_login_time"] = str(timezone.now())

            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")



def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out.")
    return redirect("login")


@login_required
def dashboard_view(request):
    return render(request, "accounts/dashboard.html")
