from audioop import reverse
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from .forms import LetterForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user  # 로그인한 사용자의 User Model객체를 반환.
from .models import Letter
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
        card.letter_to = get_user(self.request).name
        return super().form_valid(form)

class CardListView(ListView):
    def get(self, request, *args, **kwargs):
        if kwargs['username'] == get_user(request).name:
            return super().get(request, *args, **kwargs)
        else:
            return render(request,
                    "account/mailbox.html", # 호출할 template 경로
                    {'error_message':'해당 계정은 존재하지 않습니다.'}
                    )
        

    template_name = "card/mailbox.html"    
    model = Letter
    # 페이징 처리
    #  class변수: paginate_by = 한페이지의 데이터 개수
    #  요청시 url : url?page=번호   http://127.0.0.1:8000/board/list?page=2   page를 생략하면 1번페이지를 조회.
    #  페이지 번호를 template에서 출력하기 위한 값들을 만들어서 template에 전달. => get_context_data()를 오버라이딩
    paginate_by = 10  #한페이지에 10개씩 
    
    def get_queryset(self):
        # queryset = super(PostListView, self).get_queryset()
        # queryset = queryset.filter(writer=get_user(self.request).pk)
        # return queryset
        return Letter.objects.filter(letter_to=get_user(self.request).pk)

    # context data: view가 template에게 전달하는 값(dictionary). key-value쌍.  key: context name, value: context value
    # get_context_data(): Generic View를 구현할 때 template에게 추가적으로 전달해야하는 context data가 있을때 오버라이딩.
    # 페이징관련 값들을 context data에 추가
    #  - 이전/다음 페이지 그룹 유무(그룹의 시작/끝페이지)
    #  - 이전/다음 페이지 번호(그룹의 시작/끝페이지)
    #  - 현재 페이지 속한 페이지 그룹의 페이지 범위(시작 ~ 끝 페이지번호)
    def get_context_data(self, **kwargs):
        # 부모객체의 get_context_data()를 호출해서 generic view가 자동으로 생성한 Context data를 받아온다.
        context = super().get_context_data(**kwargs)
        context["total"] = len(Letter.objects.filter(letter_to=get_user(self.request).pk))
        # ListView에서 paginate_by 속성을 설정하면 context data에 Paginator객체가 등록된다.
        paginator = context['paginator']
        page_group_count = 10 #페이지그룹에 속한 페이지 개수
        current_page = int(self.request.GET.get('page', 1))
        # CBV에서 HttpRequest는 self.request로 사용할 수 있다.

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