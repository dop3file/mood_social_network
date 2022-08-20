from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from .forms import RegiserUserForm, LoginUserForm, EditProfileForm
from django.contrib.auth.decorators import login_required   
from .models import Profile
from django.contrib import messages


def get_main_page(request):
    return render(request, 'index.html')


class RegisterUser(CreateView):
    form_class = RegiserUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required 
def get_user_profile(request):
    context = {}
    context['profile'] = Profile.objects.filter(user=request.user).first()
    return render(request, 'profile.html', context=context)


@login_required
def edit_user_profile(request):
    context = {}

    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                if Profile.objects.filter(user=request.user):
                    profile = Profile.objects.get(user=request.user)
                    profile.first_name = form.cleaned_data['first_name']
                    profile.avatar = form.cleaned_data['avatar']
                    
                else:
                    profile = Profile(
                        user=request.user,
                        first_name=form.cleaned_data['first_name'],
                        avatar=form.cleaned_data['avatar']
                    )

                profile.save()
                return redirect('profile')
            except ValueError:
                messages.error(request, 'Попробуйте ещё раз')
        
    
    form = EditProfileForm
    context['form'] = form
    return render(request, 'edit_profile.html', context=context) 


def handler404(request):
    return HttpResponse('hi')