from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.urls import reverse_lazy
from django.template import TemplateDoesNotExist
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.base import TemplateView
from django.template.loader import get_template
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView  
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.signing import BadSignature
from django.core.paginator import Paginator
from django.db.models import Q

from .models import ShaUser, SubCategory, Offer
from .forms import ChangeProfileForm, RegisterUserForm, SearchForm, OfferForm, AIFormSet
from .utilities import signer
# Create your views here.


def index(request):
    offers = Offer.objects.all()
    context = {"offers": offers}
    return render(request, "main/index.html", context)


# def single(request):
#     return render(request, "main/single.html")

def by_category(request, pk):
    category = get_object_or_404(SubCategory, pk=pk)
    offers = Offer.objects.filter(is_active=True, category=pk)
    if 'keyword' in request.GET:
        keyword = request.GET["keyword"]
        q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
        offers = offers.filter(q)
    else:
        keyword = ''
    form = SearchForm(initial={'keyword': keyword})
    paginator = Paginator(offers, 20)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'category': category, 'page': page, 'offers': page.object_list, 'searchForm': form}
    return render(request, 'main/by_category.html', context)
    

def detail(request, category_pk, pk):
    offer = get_object_or_404(Offer, pk=pk)
    additional_images = offer.additionalimage_set.all()
    context = {'offer': offer, 'additional_images': additional_images}
    return render(request, 'main/detail.html', context)


def other_page(request, page):
    try:
        template = get_template('main/'+ page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


@login_required
def profile(request):
    offers = Offer.objects.filter(author=request.user.pk)
    context = {"offers": offers}
    return render(request, "main/profile.html", context)

@login_required
def profile_by_id(request, pk):
    user = get_object_or_404(ShaUser, pk=pk)
    offers = Offer.objects.filter(author=user.pk)    
    context = {"offers": offers, "user": user}
    return render(request, "main/profile.html", context)


@login_required
def add_new_offer(request):
    if request.method == 'POST':
        form = OfferForm(request.POST, request.FILES)
        if form.is_valid():
            offer = form.save()
            formset = AIFormSet(request.POST, request.FILES, instance=offer)
            if formset.is_valid():
                messages.add_message(request, messages.SUCCESS, 'Предложение добавлено')
                return redirect('main:profile')
    else:
        form = OfferForm(initial={'author': request.user.pk})
        formset = AIFormSet
        context = {'form': form, 'formset': formset}
        return render(request, 'main/add_new_offer.html', context)

    


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    user = get_object_or_404(ShaUser, username=username)
    if user.is_activated:
        template = 'main/user_is_activated.html'
    else:
        template = 'main/activation_done.html'
        user.is_active = True
        user.is_ativated = True
        user.save()
    return render(request, template)




class ShaLogin(LoginView):
    template_name = 'main/login.html'


class ShaLogout(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'

class ChangeProfileView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = ShaUser
    template_name = 'main/change_profile.html'
    form_class = ChangeProfileForm
    success_url = reverse_lazy('main:profile')
    success_message = "Профиль изменен"

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk= self.user_id)

class ShaPassChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('main:profile')
    success_message = "Пароль был изменен"

class RegisterUserView(CreateView):
    model = ShaUser
    template_name = 'main/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('main:register_done')
    
class RegisterDone(TemplateView):
    template_name = 'main/register_done.html'


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = ShaUser
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy("main:index")

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

    