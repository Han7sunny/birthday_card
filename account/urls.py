from django.urls import path
from django.views.generic import CreateView
from .forms import CustomUserCreateForm
urlpatterns = [
    path('join',CreateView.as_view(template_name='account/join_account.html',success_url='/',form_class=CustomUserCreateForm),name='join'), # 회원가입 
    # account:login로 추후 변경
    # path('login',,name='login'), # 로그인
    # path('logout',,name='logout'), # 로그아웃
]