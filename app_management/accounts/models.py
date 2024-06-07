from django.contrib.auth.models import AbstractUser, Permission
from django.db import models

class CustomUser(AbstractUser):
    points = models.IntegerField(default=0)
    groups = models.ManyToManyField('auth.Group', related_name='custom_users')
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_permissions',  # Update this line
    )