from audioop import reverse
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from .forms import LetterForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user  # 로그인한 사용자의 User Model객체를 반환.

# Create your views here.
class CreateCardView(CreateView):
    template_name = 'card/create_card.html'
    form_class = LetterForm
    success_url = reverse_lazy('card:mailbox')

    # def get_success_url(self):
    #     return reverse_lazy('card:mailbox')

    # table에 넣어줘야함
    def form_valid(self, form):
        card = form.save(commit = False) # 편지 작성
        card.letter_to = get_user(self.request)
        return super().form_valid(form)
