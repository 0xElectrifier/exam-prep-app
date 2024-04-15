from django.contrib.auth.models import AbstractBaseUser
from django.db import models
import uuid

from .managers import CustomUserManager
from core.models import BaseModel


class CustomUser(BaseModel, AbstractBaseUser):
    """
    Custom User model used for authentication classes
    """

    user_id = models.CharField(default=uuid.uuid4, editable=False, max_length=40, primary_key=True)
    username = models.CharField(max_length=40, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.email
