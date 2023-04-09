"""Django models for working with users
"""
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Custom user model
    """
