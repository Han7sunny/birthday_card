from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    name = models.CharField(verbose_name='이름', max_length=100)
    birthday = models.CharField(max_length=5, null=True) # MM/DD