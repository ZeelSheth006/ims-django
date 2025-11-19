from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(
        max_length=20,
        choices=[
            ("admin", "Admin"),
            ("manager", "Manager"),
            ("staff", "Staff"),
        ],
        default="staff"
    )
    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)

    def __str__(self):
        return self.username
