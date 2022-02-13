from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model # settings.py 에 등록된 AUTH_USER_MODEL 클래스를 반환.
from django import forms

# CustomUser와 연동된 ModelForm
class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label="ID",widget=forms.TextInput(attrs={'label':'ID','placeholder':''}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'style':'text-align:center;','placeholder':''})) # <input type='password'> # default type = 'text'
    password2 = forms.CharField(label='Password 확인', widget=forms.PasswordInput(attrs={'style':'text-align:center;','placeholder':'', 'class':'form-control'}))
    class Meta:
        model = get_user_model() # settings.py의 AUTH_USER_MODEL = 'account.CustomUser' 객체 호출
        fields = ["username", "password1", "password2", "name"]        
        widgets = {
            'username':forms.TextInput(attrs={'style':'text-align:center;','label':'ID','placeholder':''}),
            'name':forms.TextInput(attrs={'style':'text-align:center;','placeholder':''}),    
        }

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="ID",widget=forms.TextInput(attrs={'label':'ID','placeholder':''}))
    password = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'placeholder':''}))
    class Meta:
        field='__all__',