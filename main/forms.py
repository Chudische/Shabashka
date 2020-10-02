from django import forms

from .models import ShaUser

class ChangeProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Адрес электронной почты")

    class Meta:
        model = ShaUser
        fields = ('username', 'email', 'first_name', 'last_name', 'send_message')