from django.urls import path
from .views import UserCreateView, UserLoginView
from django.contrib.auth.views import LogoutView

app_name = 'account'
urlpatterns = [
    path('join', UserCreateView.as_view(),name='join'),
    path('login', UserLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]