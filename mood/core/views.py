from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from .forms import RegiserUserForm, LoginUserForm


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


def get_user_profile(request):
    if not request.user.is_authenticated:
        raise Http404
    else:
        return render(request, 'profile.html')


def handler404(request):
    return HttpResponse('hi')