from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms

# username, password1, password2 입력 받아 username과 password 등록
class CustomUserCreateForm(UserCreationForm):
    # password..
    username = forms.CharField(label='아이디')
    password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput()) # <input type='password'> # default type = 'text'
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput())
    
    class Meta:
        model = CustomUser
        fields = ["username", "password1", "password2" ,"name", "birthday"]

