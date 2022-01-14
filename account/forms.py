from dataclasses import field
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

# username, password1, password2 입력 받아 username과 password 등록
class CustomUserCreateForm(UserCreationForm):
    # password..
    class Meta:
        model = CustomUser
        field = '__all__'
