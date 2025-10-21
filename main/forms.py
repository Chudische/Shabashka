from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, Row, Column, HTML
from crispy_forms.bootstrap import PrependedText, StrictButton, InlineRadios
from django.utils.safestring import mark_safe

from .models import SuperCategory, SubCategory, Offer, AdditionalImage
from .models import Comment, UserReview, ChatMessage
from accounts.models import Location



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
       
