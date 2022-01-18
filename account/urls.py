from django.urls import path
from django.views.generic import CreateView

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreateForm

app_name = 'account' # 없으면 django.urls.exceptions.NoReverseMatch: 'account' is not a registered namespace
urlpatterns = [
    path('join',CreateView.as_view(template_name='account/join_account.html',success_url='/',form_class=CustomUserCreateForm),name='join'), # 회원가입 
    # account:login로 추후 변경,,start_form안에서 다같이 안 한다면,,
    path('login', LoginView.as_view(template_name='account/login_form.html', form_class=AuthenticationForm), name='login'), # 로그인
    path('logout', LogoutView.as_view(), name='logout'), # 로그아웃
]