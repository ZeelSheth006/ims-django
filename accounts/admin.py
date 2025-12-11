from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ("username", "email", "phone", "role", "is_staff")
    search_fields = ("username", "email", "phone")

    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("phone", "role", "profile_image")}),
    )


admin.site.register(CustomUser)
