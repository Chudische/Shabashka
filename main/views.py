from django.shortcuts import render, get_object_or_404
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

from .models import ShaUser
from .forms import ChangeProfileForm, RegisterUserForm
from .utilities import signer
# Create your views here.


def index(request):
    return render(request, "main/index.html")


# def single(request):
#     return render(request, "main/single.html")

def by_category(request, pk):
    pass


def other_page(request, page):
    try:
        template = get_template('main/'+ page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


def profile(request):
    return render(request, "main/profile.html")


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

    