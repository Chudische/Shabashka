from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, Row, Column, HTML
from crispy_forms.bootstrap import PrependedText, StrictButton, InlineRadios
from django.utils.safestring import mark_safe

from .models import Location, ShaUser, user_registrated, SuperCategory, SubCategory, Offer, AdditionalImage
from .models import Comment, ShaUserAvatar, UserReview, ChatMessage


class ChangeProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = ShaUser
        fields = ('username', 'email', 'first_name', 'last_name', 'send_message')
        

class LoginUserForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginUserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field(
                PrependedText("username",
                    mark_safe('<i class="fa fa-user"></i>'),
                    placeholder=_("Username"), autofocus="")
            ),
            Field(
                PrependedText("password",
                    mark_safe('<i class="fa fa-lock"></i>'),
                    placeholder=_("Password"))
            ),
            Div(
                StrictButton('Sign in', type='submit', css_class='btn-block btn-lg', id='id_submit'),
                css_class='form-group'
            )               
        )
    

class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(required=True)    
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False        
        self.helper.layout = Layout(
            Field(
                PrependedText("username",
                              mark_safe('<i class="fa fa-user"></i>'),
                              placeholder=_("Username"), autofocus="")
            ),
            Field(
                PrependedText("email",
                              mark_safe('<i class="fa fa-paper-plane"></i>'),
                              placeholder=_("Email"))
                
            ),
            Field(
                PrependedText("password1",
                              mark_safe('<i class="fa fa-lock"></i>'),
                              placeholder=_("Password"))
               
            ),
            Field(
                PrependedText("password2",
                              mark_safe('<i class="fa fa-lock"></i><i class="fa fa-check"></i>'),
                              placeholder=_("Confirm password"))
                
            ),
            Div(
                StrictButton('Create account', type='submit', css_class='btn-block btn-lg', id='id_submit'),
                css_class='form-group'
            )    
        )

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()        
        try:
            password1 = self.cleaned_data.get('password1')
            password2 = self.cleaned_data.get('password2')
        except:
            errors = {'password1': ValidationError(
                'Password must meet complexity requirement', code="password_invalid")}
            raise ValidationError(errors)
            
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError(
                'Passwords missmatch', code='password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registrated.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = ShaUser
        fields = ('username', 'email', 'password1', 'password2', 
            'first_name', 'last_name', 'send_message')
        widgets ={
            "username": forms.TextInput(attrs={"placeholder": "Username"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
            "password1": forms.PasswordInput(attrs={"placeholder": "Password"}),
            "password2": forms.PasswordInput(attrs={"placeholder": "Confirm password"})

        }


class SubCategoryForm(forms.ModelForm):
    super_category = forms.ModelChoiceField(queryset=SuperCategory.objects.all(),
                    empty_label=None, label="Super category", required=True)

    class Meta:
        model = SubCategory
        fields = '__all__'


class SearchForm(forms.Form):
    keyword = forms.CharField(required=False, max_length=20, label='',
                              widget=forms.TextInput(attrs={"placeholder": "Search"}))

    
class OfferForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):    
        super(OfferForm, self).__init__(*args, **kwargs)
        self.fields["category"].help_text = 'Chose category'
        self.fields["title"].help_text = 'Description. Write here what is needed to be done'
        self.fields["price"].help_text = 'Preferable price'
        self.fields["image"].help_text = 'Main photo'

    class Meta:
        model = Offer        
        exclude = ['reviews', 'shared', 'status', "is_active", 'winner']
        widgets = {'author': forms.HiddenInput}


AIFormSet = forms.inlineformset_factory(Offer, AdditionalImage, fields='__all__')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'offer', 'price', 'time_amount', 'measure', 'content')
        exclude = ("is_active", )
        widgets = {
            "offer": forms.HiddenInput,
            "author": forms.HiddenInput,
            'content': forms.Textarea(attrs={'rows': 4})
        }
                   

class AvatarForm(forms.ModelForm):
    class Meta:       
        model = ShaUserAvatar
        fields = "__all__"
        widgets = {
            "user": forms.HiddenInput
        }


class UserReviewForm(forms.ModelForm):    

    def __init__(self, *args, **kwargs):
        super(UserReviewForm, self).__init__(*args, **kwargs)
        self.fields["content"].initial = "Deal has been completed successfully!"
        self.helper = FormHelper()               
        self.helper.layout = Layout(
            Field(
                'author'
            ),
            Field(
                'reviewal'
            ),
            Field(
                'offer'
            ),
            Div(
                InlineRadios('speed')
            ),
            Div(
                InlineRadios('cost')
            ),
            Div(
                InlineRadios('accuracy')
            ),
            Field(
                'content', rows="5"
               
            ), 
           StrictButton('Send', type='submit', css_class='btn btn-primary')
        )

    class Meta:
        model = UserReview
        fields = ('author', 'reviewal', 'offer', 'speed', 'cost', 'accuracy', 'content')
        widgets = {
            'author': forms.HiddenInput,
            'reviewal': forms.HiddenInput,
            'offer': forms.HiddenInput,
            'speed': forms.RadioSelect,
            'cost': forms.RadioSelect,
            'accuracy': forms.RadioSelect
        }


class ChatMessageForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(ChatMessageForm, self).__init__(*args, **kwargs)              
        self.helper = FormHelper()               
        self.helper.layout = Layout(
            Field('author'),
            Field('offer'),
            Field('receiver'),
            Field('content', rows=3),
            Submit('submit', 'Send')

        )

    class Meta:
        model = ChatMessage
        fields = ('author', 'offer', 'receiver', 'content')
        widgets = {
            "author": forms.HiddenInput,
            "offer": forms.HiddenInput,
            "receiver": forms.HiddenInput,
        }
       

class LocationForm(forms.ModelForm):

    class Meta:
        model = Location
        fields = ('search_id', 'name')
        widgets = {
            'search_id': forms.HiddenInput,
            'name': forms.TextInput(attrs={'list': 'locations', 'class': 'form-control', 'autocomplete': 'off'}),
        }


LocationFormSet = forms.inlineformset_factory(Offer, Location, form=LocationForm, fields=('search_id', 'name'), can_delete=False)