from django.contrib.auth.models import AbstractUser
from django.db import models


# AbstractUser class also had 'is_active' field
# Just found it out =D
# Anyway, I think it's more comfy to work with custom user class and better practice
class User(AbstractUser):
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['username']


class RefreshToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokens')
    refresh_token = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    exp_time = models.IntegerField()  # in days
