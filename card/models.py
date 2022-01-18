from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Letter(models.Model):
    # 작성자 # 나중에 생일 지나고 나서 확인할 때 작성자 홈페이지도 있으면 이동?
    # 작성자 비밀번호
    # 작성일시
    # 내용
    writer = models.CharField(verbose_name='작성자', max_length=20, primary_key=True)
    password = models.CharField(verbose_name='비밀번호', max_length=10)
    content = models.TextField(verbose_name='편지 내용') #TextField: 대용량 text
    #작성일시. auto_now_add=True(기본값:False) => insert 시점의 일시를 저장하고 그 이후에는 update하지 않음.
    create_at = models.DateTimeField(verbose_name='작성일시', auto_now_add=True)
    #수정일시. auto_now=True(기본값:False) -> insert/update 할 때마다 그 시점의 일시를 저장.
    update_at = models.DateTimeField(verbose_name='수정일시', auto_now=True)
