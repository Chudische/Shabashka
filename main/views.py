from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseNotAllowed
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
from django.db.models import Q, Avg, fields
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from extra_views import UpdateWithInlinesView, InlineFormSetFactory

from .models import Location, ShaUser, SubCategory, Offer, Comment, ShaUserAvatar, UserReview, ChatMessage
from .forms import ChangeProfileForm, RegisterUserForm, SearchForm, OfferForm, AIFormSet, CommentForm
from .forms import AvatarForm, LoginUserForm, UserReviewForm, ChatMessageForm, LocationForm, LocationFormSet
from .utilities import signer


def index(request):
    offers = Offer.objects.filter(is_active=True)
    paginator = Paginator(offers, 30)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    if 'keyword' in request.GET:
        keyword = request.GET["keyword"]
        q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
        offers = offers.filter(q)
    else:
        keyword = ''
    form = SearchForm(initial={'keyword': keyword})
    context = {"offers": offers, "page": page, 'searchForm': form}     
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


@login_required
def favorite(request):    
    users = [user for user in request.user.favorite.all()]    
    offers = Offer.objects.filter(is_active=True, author__in=users).order_by("-created")
    paginator = Paginator(offers, 30)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {"offers": offers, "page": page}
    return render(request, 'main/favorite.html', context)


def detail(request, category_pk, pk):
    offer = get_object_or_404(Offer, pk=pk)
    offer.reviews += 1
    offer.save()
    additional_images = offer.additionalimage_set.all()
    comments = Comment.objects.filter(offer=pk, is_active=True)
    form = CommentForm(initial={'offer': offer, "author": request.user})
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.save()
            messages.add_message(request, messages.SUCCESS, "Comment has been added")
        else:
            form = comment_form
            messages.add_message(request, messages.WARNING, "Comment has not been added")

    context = {'offer': offer, 
               'additional_images': additional_images,
               'comments': comments, 
               'form': form}
    return render(request, 'main/detail.html', context)


def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


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
    return render(request, "main/profile.html", context)


@login_required
def profile_by_id(request, pk):
    user = get_object_or_404(ShaUser, pk=pk)
    if user == request.user:        
        return redirect("main:profile")   
    reviews = user.rating.count()
    offers = Offer.objects.filter(author=user.pk)    
    context = {"offers": offers, "user": user, 'reviews': reviews}
    return render(request, "main/profile.html", context)


@login_required
def add_new_offer(request):
    if request.method == 'POST':
        form = OfferForm(request.POST, request.FILES)
        if form.is_valid():
            offer = form.save()
            formset = AIFormSet(request.POST, request.FILES, instance=offer)
            location_formset = LocationFormSet(request.POST, request.FILES, instance=offer) 
            if formset.is_valid() and location_formset.is_valid():
                messages.add_message(request, messages.SUCCESS, 'Offer has been posted')
                return redirect('main:profile')
    else:
        form = OfferForm(initial={'author': request.user.pk})
        formset = AIFormSet
        try:
            location_formset = LocationFormSet(
                initial=[{'name': request.user.location, 'search_id': request.user.location.search_id }]
                )
        except ShaUser.location.RelatedObjectDoesNotExist:
            location_formset = LocationFormSet()        
        context = {'form': form, 'formset': formset, 'location': location_formset}
        return render(request, 'main/add_new_offer.html', context)


@login_required
def offer_change(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
    if request.user != offer.author:
        messages.add_message(request, messages.ERROR, "You can edit only your own offers!")
        return redirect("main:profile")
    if request.method == "POST":
        form = OfferForm(request.POST, request.FILES, instance=offer)
        if form.is_valid():
            offer = form.save()
            formset = AIFormSet(request.POST, request.FILES, instance=offer)
            location_formset = LocationFormSet(request.POST, request.FILES, instance=offer)           
            if formset.is_valid() and location_formset.is_valid():
                formset.save()
                location_formset.save()
                messages.add_message(request, messages.SUCCESS, "Offer successfully updated")
                return redirect("main:profile")
    else:
        form = OfferForm(instance=offer)
        formset = AIFormSet(instance=offer)
        location_formset = LocationFormSet(
                instance=offer, 
                initial=[{'name': request.user.location, 'search_id': request.user.location.search_id}]
                )
        context = {'offer': offer, 'form': form, 'formset': formset, "location": location_formset}
        return render(request, "main/change_offer.html", context)


@login_required
def offer_delete(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
    if request.user != offer.author:
        messages.add_message(request, messages.ERROR, "You can delete only your own offers!")
        return redirect("main:profile")
    if request.method == "POST":
        offer.delete()
        messages.add_message(request, messages.SUCCESS, "Offer successfully deleted")
        return redirect("main:profile")
    else:
        context = {'offer': offer}
        return render(request, "main/delete_offer.html", context)


@login_required
def reviews(request, user_id):
    user = get_object_or_404(ShaUser, pk=user_id)
    reviews = UserReview.objects.filter(reviewal=user)
    context = {
        'user': user,
        'reviews': reviews
    }
    
    return render(request, 'main/reviews.html', context) 


@login_required
def chat(request, offer_pk):
    offer = get_object_or_404(Offer, pk=offer_pk)    
    if request.user != offer.author:
        if request.user != offer.winner:
            raise PermissionDenied
    if request.method == 'POST':
        message_form = ChatMessageForm(request.POST)
        if message_form.is_valid():
            message_form.save()
            messages.add_message(request, messages.SUCCESS, "Message sent")
    receiver = offer.winner if request.user == offer.author else offer.author
    form = ChatMessageForm(initial={
        'author': request.user, 
        'offer': offer,
        'receiver': receiver
        })
    chat_messages = offer.chat_messages.all()
    context = {
        "offer": offer,
        "chat_messages": chat_messages,
        'form': form
    }
    return render(request, 'main/chat_messages.html', context)


@login_required
def chat_list(request):
    user = request.user
    q = Q(author=user) | Q(receiver=user)
    user_chats = ChatMessage.objects.filter(q)
    context = {
        "user_chats": user_chats
    }
    return render(request, 'main/chat_list.html', context)


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
        user.is_activated = True
        user.save()
    return render(request, template)


class UserReviewView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = 'main/user_review.html'
    form_class = UserReviewForm
    success_message = 'Congratulations! The offer was successfully completed.'
    success_url = reverse_lazy('main:profile')

    def get_initial(self, *args, **kwargs):
        author = self.request.user
        reviewal = self.kwargs['user_pk']
        offer = self.kwargs['offer_pk']
        return {
            'author': author,
            'reviewal': reviewal,
            'offer': offer
        }   


class ShaLogin(LoginView):
    template_name = 'main/login.html'
    form_class = LoginUserForm
   

class ShaLogout(SuccessMessageMixin, LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'
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
    template_name = 'main/change_profile.html'
    inlines = [LocationInline, ]    
    form_class = ChangeProfileForm
    success_url = reverse_lazy('main:profile')
    success_message = "Profile updated"

    def dispatch(self, request, *args, **kwargs):        
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()        
        return get_object_or_404(queryset, pk=self.user_id)


class ShaPassChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('main:profile')
    success_message = "Password successfully updated"


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
        messages.add_message(request, messages.SUCCESS, 'User was successfully deleted')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)



