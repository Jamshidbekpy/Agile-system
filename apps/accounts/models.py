from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class Role(models.TextChoices):
    PROJECT_OWNER = "project_owner", _("Project Owner")
    PROJECT_MANAGER = "project_manager", _("Project Manager")
    DEVELOPER = "developer", _("Developer")
    TESTER = "tester", _("Tester")


class User(AbstractUser):
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.DEVELOPER)

    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
