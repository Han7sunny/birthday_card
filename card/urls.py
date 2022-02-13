from django.urls import path
from card.views import CardCreateView, CardAuthView, CardDetailView, CardUpdateView, card_delete

app_name = 'card'
urlpatterns = [
    path('create', CardCreateView.as_view(), name='create'), #글 등록 View url
    path('auth/<str:pk>',CardAuthView, name='auth'), # 작성자 열람
    path('detail/<str:pk>',CardDetailView.as_view(), name='detail'), #게시물 상세페이지
    path('update/<str:pk>', CardUpdateView.as_view(), name='update'), #글 수정 url. GET: 수정할 게시물의 pk을 path parameter 받아야함.
    path('delete/<str:pk>', card_delete, name='delete'), #삭제처리.
]