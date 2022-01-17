from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# username, password, birthday
class CustomUser(AbstractUser):
    name = models.CharField(verbose_name='닉네임', max_length=20) # 생일 당사자
    birthday = models.DateField(verbose_name='생년월일') # 20XXXXXX ,max_length=8
