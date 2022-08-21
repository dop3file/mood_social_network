from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from .forms import RegiserUserForm, LoginUserForm, EditProfileForm
from django.contrib.auth.decorators import login_required   
from .models import Profile
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


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

        try:
            profile = Profile.objects.get(user=request.user)
        except ObjectDoesNotExist:
            profile = Profile(user=request.user)

        form = EditProfileForm(instance=profile, data=request.POST, files=request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect('profile')
            except ValueError:
                messages.error(request, 'Попробуйте ещё раз')

    form = EditProfileForm

    if Profile.objects.filter(user=request.user).first():
        profile = Profile.objects.get(user=request.user)
        context['profile'] = Profile.objects.filter(user=request.user).first()
        form = EditProfileForm(initial={'first_name': profile.first_name, 'surname': profile.surname})
    
    context['form'] = form
    
    return render(request, 'edit_profile.html', context=context) 


def handler404(request):
    return HttpResponse('hi')