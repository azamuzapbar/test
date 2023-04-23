from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    email = forms.CharField(required=True, label='Логин')
    password = forms.CharField(required=True, label='Пароль', widget=forms.PasswordInput)


GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
)


class CustomUserCreationForm(forms.ModelForm):
    username = forms.CharField(min_length=5, max_length=50,
                               widget=forms.TextInput, required=True)
    email = forms.CharField(min_length=7, max_length=70, required=True,
                            widget=forms.EmailInput)
    avatar = forms.ImageField(required=True)
    password = forms.CharField(label='Пароль', strip=False, required=True, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Подтвердите пароль', strip=False, required=True,
                                       widget=forms.PasswordInput)
    gender = forms.ChoiceField(label='Пол', choices=GENDER_CHOICES, widget=forms.RadioSelect())

    class Meta:
        model = get_user_model()
        fields = (
            'username', 'email', 'avatar', 'password', 'password_confirm', 'username', 'info', 'phone_number',
            'gender')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise ValidationError('Пароли не совпадают')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'info', 'phone_number', 'email', 'avatar', 'gender','birth_date')
