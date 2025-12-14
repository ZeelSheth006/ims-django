from django.contrib import admin
from django.urls import path, include
from inventory.views import dashboard

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", dashboard, name="dashboard"),  # 👈 THIS FIXES 404
    path("accounts/", include("accounts.urls")),
    path("inventory/", include("inventory.urls")),
    path("purchases/", include("purchases.urls")),
    path("sales/", include("sales.urls")),
    path("reports/", include("reports.urls")),
]
