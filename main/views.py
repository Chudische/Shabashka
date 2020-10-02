from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.urls import reverse_lazy
from django.template import TemplateDoesNotExist
from django.views.generic.edit import UpdateView
from django.template.loader import get_template
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from .models import ShaUser
from .forms import ChangeProfileForm
# Create your views here.


def index(request):
    return render(request, "main/index.html")


# def single(request):
#     return render(request, "main/single.html")


def other_page(request, page):
    try:
        template = get_template('main/'+ page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


def profile(request):
    return render(request, "main/profile.html")


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



    