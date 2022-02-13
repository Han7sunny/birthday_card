# account/views.py
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user  # 로그인한 사용자의 User Model객체를 반환.
from .forms import CustomUserCreationForm, CustomAuthenticationForm

# 가입 View
class UserCreateView(CreateView):
    template_name = "account/join_form.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('account:login')
    
    def post(self, request, *args, **kwargs):
        if self.get_form().data['day'] == 'default':
            return render(request,"account/join_form.html"
            ,{"birthday_error":"생일을 입력해 주세요.", "form":self.get_form()})
        else:
            return super().post(request, *args, **kwargs)
    
    def form_valid(self,  form): # 등록 / 수정
        account = form.save(commit=False)  #ModelForm.save() : insert 후에 insert한 Model 객체가 반환
        account.birthday = form.data.get('month')+"/"+form.data.get('day')
        return super().form_valid(form)

# 로그인 처리 View
class UserLoginView(LoginView):
    template_name = 'account/login_form.html'
    form_class = CustomAuthenticationForm
    
    def get_success_url(self):
        if self.request.path_info.endswith('relogin') and self.request.path_info.split('/')[1] == self.get_form().data['username']:
            self.request.session['birthday'] = get_user(self.request).username
        return reverse_lazy('login_user', args=[get_user(self.request).username])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.path_info.endswith('relogin'):
            context["relogin"] = get_user(self.request).username
        return context