from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile


class RegiserUserForm(UserCreationForm):
    username = forms.CharField(
        label='Логин', 
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    email = forms.EmailField(
        label='Email', 
        widget=forms.EmailInput(attrs={'class': 'form-control'}))

    password1 = forms.CharField(
        label='Пароль', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}))

    password2 = forms.CharField(
        label='Пароль', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', 
    widget=forms.TextInput(attrs={'class': 'form-control'}))

    password = forms.CharField(label='Пароль', 
    widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}))


class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(
                    label='Имя', 
                    max_length=30,
                    widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'exampleFormControlInput1', 'placeholder': 'Имя', 'name': 'first_name'}),
                    required=False
                    )
    surname = forms.CharField(
                    label='Фамилия', 
                    max_length=40,
                    widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'exampleFormControlInput1', 'placeholder': 'Фамилия', 'name': 'surname'}),
                    required=False
                    )
    avatar = forms.FileField(
                    label='Аватарка', 
                    widget=forms.FileInput(attrs={'class': 'form-control', 'id': 'exampleFormControlInput1', 'placeholder': 'Аватарка', 'name': 'avatar'}),
                    required=False
                    )
    vk_social_link = forms.CharField(
                    label='VK',
                    max_length=150,
                    widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'exampleFormControlInput1', 'placeholder': 'Ссылка на VK', 'name': 'vk_social_link'}),
                    required=False
                    )

    class Meta:
        model = Profile
        fields = ['first_name', 'surname', 'avatar', 'vk_social_link']


