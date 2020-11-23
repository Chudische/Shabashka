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
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.signing import BadSignature
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist


from .models import ShaUser, SubCategory, Offer, Comment
from .forms import ChangeProfileForm, RegisterUserForm, SearchForm, OfferForm, AIFormSet, CommetForm
from .forms import PasswordRegenerationForm 
from .utilities import signer, send_password_restore_link
# Create your views here.


def index(request):
    offers = Offer.objects.all()
    paginator = Paginator(offers, 30)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {"offers": offers, "page": page}
    return render(request, "main/index.html", context)


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
    paginator = Paginator(offers, 30)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'category': category, 'page': page, 'offers': page.object_list, 'searchForm': form}
    return render(request, 'main/by_category.html', context)
    

def detail(request, category_pk, pk):
    offer = get_object_or_404(Offer, pk=pk)
    offer.reviews += 1
    offer.save()
    additional_images = offer.additionalimage_set.all()
    comments = Comment.objects.filter(offer=pk, is_active=True)
    form = CommetForm(initial={'offer': offer, "author": request.user})
    if request.method == "POST":
        comment_form = CommetForm(request.POST)
        if comment_form.is_valid():
            comment_form.save()
            messages.add_message(request, messages.SUCCESS, "Коментарий добавлен")
        else:
            form = comment_form
            messages.add_message(request, messages.WARNING, "Коментарий не добавлен")

            
    context = {'offer': offer, 
               'additional_images': additional_images,
               'comments': comments, 
               'form': form}
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


@login_required
def offer_change(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
    if request.user != offer.author:
        messages.add_message(request, messages.ERROR, "Вы можете управлять только своими предложениями")
        return redirect("main:profile")
    if request.method == "POST":
        form = OfferForm(request.POST, request.FILES, instance=offer)
        if form.is_valid():
            offer = form.save()
            formset = AIFormSet(request.POST, request.FILES, instance=offer)
            if formset.is_valid():
                formset.save()
                messages.add_message(request, messages.SUCCESS, "Предложение исправлено")
                return redirect("main:profile")
    else:
        form = OfferForm(instance=offer)
        formset = AIFormSet(instance=offer)
        context = {'form': form, 'formset': formset}
        return render(request, "main/change_offer.html", context)


@login_required
def offer_delete(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
    if request.user != offer.author:
        messages.add_message(request, messages.ERROR, "Вы можете управлять только своими предложениями")
        return redirect("main:profile")
    if request.method == "POST":
        offer.delete()
        messages.add_message(request, messages.SUCCESS, "Предложение удалено")
        return redirect("main:profile")
    else:
        context = {'offer': offer}
        return render(request, "main/delete_offer.html", context)

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
   

class ShaLogout(SuccessMessageMixin, LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'
    next_page = 'main:index'
   
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
             messages.add_message(request, messages.SUCCESS, "Вы успешно вышли. До новых встреч!")
        return super().dispatch(request, *args, **kwargs)

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

class ShaPassResetView(PasswordResetView):
    template_name = 'main/password_reset.html'
    email_template_name = 'main/password_reset_email.html'
    email_subject_name = 'main/password_reset_email_subject.html'
    success_url = reverse_lazy('main:password_reset_done')

class ShaPassResetDoneView(PasswordResetDoneView):
    template_name = 'main/password_reset_sent.html'

class ShaPassResetConfirmView(PasswordResetConfirmView):
    template_name = 'main/password_regenerate.html'
    success_url = reverse_lazy('main:password_reset_complete')


class ShaPassResetCompleteView(PasswordResetCompleteView):
    template_name = 'main/password_reset_done.html'

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

