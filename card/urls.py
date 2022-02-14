from django.urls import path
from card.views import CardCreateView, CardAuthView, CardDetailView, CardUpdateView, card_delete

app_name = 'card'
urlpatterns = [
    path('create', CardCreateView.as_view(), name='create'),
    path('auth/<str:pk>',CardAuthView, name='auth'),
    path('detail/<str:pk>',CardDetailView.as_view(), name='detail'), 
    path('update/<str:pk>', CardUpdateView.as_view(), name='update'), 
    path('delete/<str:pk>', card_delete, name='delete'), 
]