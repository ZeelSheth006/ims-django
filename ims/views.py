from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render

def home(request):
    return HttpResponse("<h1>Welcome to Inventory Management System</h1>")

def home(request):
    return redirect("/accounts/login/")

def home(request):
    last_login = request.session.get("last_login_time", "First Login")
    return render(request, "home.html", {"last_login": last_login})
