# card/views.py
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.urls import reverse_lazy, reverse

from .forms import CardForm
from .models import Card

from django.contrib.auth.decorators import login_required # 로그인여부를 확인해서 로그인 안한경우 settings.py의 LOGIN_URL의 경로로 이동.
from django.utils.decorators import method_decorator # class의 메소드에 decorator를 선언해 주는 decorator
from django.contrib.auth import get_user  # 로그인한 사용자의 User Model객체를 반환.

@method_decorator(login_required, name='dispatch') 
class CardCreateView(CreateView):
    template_name = 'card/card_create.html'
    form_class = CardForm

    def get(self, request, *args, **kwargs):
        if kwargs['username'] == get_user(request).username:
            return super().get(request, *args, **kwargs)
        else:
            return render(request,
                        "account/error.html",
                        {'error_message':'해당 계정은 존재하지 않습니다. 계정을 생성해 주세요.'}
                        )

    def post(self, request, *args, **kwargs):
        request.POST._mutable = 'True' 
        self.get_form().data.update({"card_from":self.get_form().data['card_from']+"_"+str(get_user(request).pk)})
        return super().post(request, *args, **kwargs)
    
    def get_success_url(self): # 등록 / 수정 / 삭제 후 이동할 url 정의
        messages.info(self.request, '편지가 정상적으로 등록되었습니다.')
        return reverse_lazy('card:detail', args=[get_user(self.request).username, self.object.card_from]) # args: path parameter로 전달할 값들을 리스트에 순서대로 담는다.

    def form_valid(self,  form): # 등록 / 수정
        card = form.save(commit=False)  #ModelForm.save() : insert 후에 insert한 Model 객체가 반환
        # commit = false : 일단 모델만 가져옴. 가상 insert 아직 DB에 안 들어감
        card.card_to = get_user(self.request)  #로그인한 User객체
        return super().form_valid(form)
    
    def form_invalid(self, form): # 보내는 이 이미 존재한다면
        form.data['card_from'] = form.data.get('card_from').split('_')[0] 
        return super().form_invalid(form)


def CardAuthView(request, username, pk):
    if username == get_user(request).username: 
        if request.method == 'GET':
            return render(request,"card/card_auth.html",{'card_from':pk})
        elif request.method == 'POST':
            input_pw = request.POST.get('input_password')
            check = Card.objects.get(pk=pk)

            if input_pw == check.password:
                return redirect(reverse('card:detail', args=[get_user(request).username, pk]))
            else:
                return render(request,
                    "card/card_auth.html",
                    {'error_message':'해당 계정은 존재하지 않습니다.'}
                    )
    else:
        return render(request,"account/error.html",
                    {'error_message':'해당 계정은 존재하지 않습니다. 계정을 생성해 주세요.'}
                    )

class CardDetailView(DetailView):
    template_name = "card/card_detail.html"
    model = Card 

    def get(self, request, *args, **kwargs):
        if kwargs['username'] != get_user(request).username:
            return render(request,
                    "account/error.html",
                    {'error_message':'해당 계정은 존재하지 않습니다. 계정을 생성해 주세요.'}
                    )
        return super().get(request, *args, **kwargs)

@method_decorator(login_required, 'dispatch')
class CardUpdateView(UpdateView):
    template_name = "card/card_update.html"
    form_class = CardForm
    model = Card
    
    def get(self, request, *args, **kwargs):
        if kwargs['username'] != get_user(request).username:
            return render(request,
                    "account/error.html", # 호출할 template 경로
                    {'error_message':'해당 계정은 존재하지 않습니다. 계정을 생성해 주세요.'}
                    )
        try:
            card =  Card.objects.get(pk=kwargs["pk"])
        except Card.DoesNotExist:
            return render(request,
                    "account/error.html",
                    {'error_message':'이미 삭제된 편지입니다.'}
                    )
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request.POST._mutable = 'True' 
        self.get_form().data.update({"card_from":self.get_form().data['card_from']+"_"+str(get_user(request).pk)})
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('card:detail', args=[get_user(self.request).username, self.object.pk])

@login_required
def card_delete(request, username, pk):
    if username == get_user(request).username:   
        try:
            card = Card.objects.get(pk=pk) 
            card.delete()        
            messages.info(request, '편지가 정상적으로 삭제되었습니다.')
        except Card.DoesNotExist:
            return render(request,
                    "account/error.html",
                    {'error_message':'이미 삭제된 편지입니다.'}
                    )
        return redirect(reverse('login_user', args=[get_user(request).username]))
    else:
        return render(request,
                    "account/error.html",
                    {'error_message':'해당 계정은 존재하지 않습니다. 계정을 생성해 주세요.'}
                    )

@method_decorator(login_required, 'dispatch') # 추가 for 계정의 글 목록
class CardListView(ListView):
    template_name = "card/card_list.html"    
    model = Card
    paginate_by = 10  #한페이지에 10개씩 

    def get(self, request, *args, **kwargs):
        if kwargs['username'] == get_user(request).username:
            return super().get(request, *args, **kwargs)
        else:
            return render(request,
                    "account/error.html",
                    {'error_message':'해당 계정은 존재하지 않습니다. 계정을 생성해 주세요.'}
                    )

    def get_queryset(self):
        return Card.objects.filter(card_to=get_user(self.request).pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.session.get('birthday'):
            context['birthday'] = True
       
        context["total"] = len(Card.objects.filter(card_to=get_user(self.request).pk))
        paginator = context['paginator']
        page_group_count = 10 
        current_page = int(self.request.GET.get('page', 1))

        # 페이지 그룹의 페이지 범위 조회
        start_idx = int((current_page-1)/page_group_count)*page_group_count
        end_idx = start_idx + page_group_count
        page_range = paginator.page_range[start_idx : end_idx]

        # 그룹의 시작 페이지가 이전페이지가 있는지, 그룹의 마지막 페이지가 다음페이지가 있는지 여부 + 페이지 번호
        start_page = paginator.page(page_range[0]) #시작 페이지의 Page객체
        end_page = paginator.page(page_range[-1]) # 마지막 페이지의 Page객체

        has_previous = start_page.has_previous() #시작의 이전페이지가 있는지 여부
        has_next = end_page.has_next() # 마지막 페이지의 다음 페이지가 있는지 여부

        context['page_range'] = page_range
        if has_previous:
            context['has_previous'] = has_previous
            context['previous_page_no'] = start_page.previous_page_number  #시작페이지의 이전 페이지 번호

        if has_next:
            context['has_next'] = has_next
            context['next_page_no'] = end_page.next_page_number #마지막 페이지의 다음 페이지 번호

        return context
