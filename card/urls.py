from django.urls import path
from django.views.generic import TemplateView, CreateView
from .views import CreateCardView

app_name='card'
urlpatterns=[
    path('mailbox',TemplateView.as_view(template_name='card/mailbox.html'),name='mailbox'),
    path('create',CreateCardView.as_view(),name='create'),
]