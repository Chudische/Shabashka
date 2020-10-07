from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from .models import ShaUser, user_registrated, SuperCategory, SubCategory

class ChangeProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Адрес электронной почты")

    class Meta:
        model = ShaUser
        fields = ('username', 'email', 'first_name', 'last_name', 'send_message')

class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Адрес электронной почты")
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput, 
        help_text=password_validation._password_validators_help_text_html()
    )
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput, 
        help_text="Введите Ваш пароль повторно"
    )

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError(
                'Введенные пароли не совпадают', code='password_mismath')}
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


class SubCategoryForm(forms.ModelForm):
    super_category = forms.ModelChoiceField(queryset=SuperCategory.objects.all(),
                    empty_label=None, label="Надкатегория", required=True)
    class Meta:
        model = SubCategory
        fields = '__all__'