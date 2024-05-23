from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    USER_TYPE_CHOICES = [("admin", "Admin"), ("user", "User")]
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True)
    user_type = models.CharField(
        _("User Type"), blank=True, max_length=255, choices=USER_TYPE_CHOICES
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
