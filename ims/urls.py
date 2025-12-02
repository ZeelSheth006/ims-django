from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from ims.views import home
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home page
    path('', home, name='home'),

    # Apps
    path('accounts/', include('accounts.urls')),
    path('inventory/', include('inventory.urls')),
    path('purchases/', include('purchases.urls')),
    path('sales/', include('sales.urls')),
    path("", home, name="dashboard"),
    path('', lambda request: redirect('dashboard')),
    path("products/", include("inventory.urls")),
    path("purchases/", include("purchases.urls")),
    path("sales/", include("sales.urls")),
    path("something/", redirect, name="something"),






]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
