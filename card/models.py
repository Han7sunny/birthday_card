from django.db import models
from account.models import CustomUser

class Card(models.Model):
    card_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField(verbose_name='편지 내용') 
    card_from = models.CharField(verbose_name='보내는 사람', max_length=10, unique=True, primary_key=True)
    password = models.CharField(verbose_name='비밀번호',max_length=10, default=None)
    create_at = models.DateTimeField(verbose_name='작성일시', auto_now_add=True)
    update_at = models.DateTimeField(verbose_name='수정일시', auto_now=True)

    class Meta:
        ordering = ["-create_at"]