from django.urls import path
from .views import add_sale, sale_list

urlpatterns = [
    path("add/", add_sale, name="add_sale"),
    path("list/", sale_list, name="sale_list"),
]
