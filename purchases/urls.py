from django.urls import path
from .views import add_purchase, purchase_list

urlpatterns = [
    path("add/", add_purchase, name="add_purchase"),
    path("list/", purchase_list, name="purchase_list"),
]
