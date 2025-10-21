from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.signing import BadSignature
from extra_views import UpdateWithInlinesView, InlineFormSetFactory

from .models import ShaUser, ShaUserAvatar, Location
from .forms import ChangeProfileForm, RegisterUserForm, AvatarForm, LoginUserForm, LocationForm, LocationFormSet
from main.utilities import signer
from main.models import Offer


@login_required
def profile(request):
    if request.method == "POST":
        instance, created = ShaUserAvatar.objects.get_or_create(user=request.user)
        avatar_form = AvatarForm(request.POST, request.FILES, instance=instance)
        if avatar_form.is_valid():
            avatar_form.save()
            messages.add_message(request, messages.SUCCESS, 'Profile photo has been updated')
        else:
            messages.add_message(request, messages.ERROR, 'Error! File not supported.')
    else:
        avatar_form = AvatarForm(initial={"user": request.user})    
    offers = Offer.objects.filter(author=request.user.pk)    
    reviews = request.user.rating.count()  
    context = {"offers": offers, "avatar_form": avatar_form, 'reviews': reviews}   
    return render(request, "accounts/profile.html", context)


@login_required
def profile_by_id(request, pk):
    user = get_object_or_404(ShaUser, pk=pk)
    if user == request.user:        
        return redirect("accounts:profile")   
    reviews = user.rating.count()
    offers = Offer.objects.filter(author=user.pk)    
    context = {"offers": offers, "user": user, 'reviews': reviews}
    return render(request, "accounts/profile.html", context)


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    user = get_object_or_404(ShaUser, username=username)
    if user.is_activated:
        template = 'accounts/user_is_activated.html'
    else:
        template = 'accounts/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


class ShaLogin(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginUserForm
   

class ShaLogout(SuccessMessageMixin, LoginRequiredMixin, LogoutView):
    template_name = 'accounts/logout.html'
    next_page = 'main:index'
   
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
             messages.add_message(request, messages.SUCCESS, "Logged out. See you later")
        return super().dispatch(request, *args, **kwargs)


class LocationInline(InlineFormSetFactory):
    model = Location
    form_class = LocationForm
    fields = ('search_id', 'name')
    factory_kwargs = {'can_delete': False}


class ChangeProfileView(SuccessMessageMixin, LoginRequiredMixin, UpdateWithInlinesView):
    model = ShaUser
    template_name = 'accounts/change_profile.html'
    inlines = [LocationInline, ]    
    form_class = ChangeProfileForm
    success_url = reverse_lazy('accounts:profile')
    success_message = "Profile updated"

    def dispatch(self, request, *args, **kwargs):        
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()        
        return get_object_or_404(queryset, pk=self.user_id)


class ShaPassChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('accounts:profile')
    success_message = "Password successfully updated"


class ShaPassResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    email_subject_name = 'accounts/password_reset_email_subject.html'
    success_url = reverse_lazy('accounts:password_reset_done')


class ShaPassResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_sent.html'


class ShaPassResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_regenerate.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class ShaPassResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_done.html'


class RegisterUserView(CreateView):
    model = ShaUser
    template_name = 'accounts/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('accounts:register_done')


class RegisterDone(TemplateView):
    template_name = 'accounts/register_done.html'


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = ShaUser
    template_name = 'accounts/delete_user.html'
    success_url = reverse_lazy("main:index")

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'User was successfully deleted')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)