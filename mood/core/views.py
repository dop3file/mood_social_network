from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required   

from .utils import search_post, generate_default_avatar
from .controllers import *
from .models import Profile, Interest
from .forms import RegiserUserForm, LoginUserForm, EditProfileForm


def get_main_page(request):
    context = main_page_controller(request)

    return render(request, 'index.html', context=context)


class RegisterUser(CreateView):
    form_class = RegiserUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def form_valid(self, form):
        user = form.save()
        profile = Profile(user=user)
        profile.avatar = generate_default_avatar(user.username)
        profile.save()
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


def get_profile(request, username):
    context = get_profile_controller(request, username)

    return render(request, 'profile.html', context=context)
    

@login_required
def edit_user_profile(request):
    context = {}
    context['profile'] = get_object_or_404(Profile, user=request.user)
    context['interests'] = Interest.objects.filter(user=context['profile']).all()

    if request.method == "POST":
        try:
            edit_user_profile_controller(request, context)
        except ValueError:
            messages.error(request, 'Попробуйте ещё раз')
        return redirect('profile', username=request.user.username)

    form = EditProfileForm

    if Profile.objects.filter(user=request.user).first():
        profile = Profile.objects.get(user=request.user)
        context['profile'] = Profile.objects.filter(user=request.user).first()
        form = EditProfileForm(initial={
                                'first_name': profile.first_name, 
                                'surname': profile.surname,
                                'vk_social_link': profile.vk_social_link,
                                'github_social_link': profile.github_social_link
                                })
    
    context['form'] = form
    
    return render(request, 'edit_profile.html', context=context)


@login_required
def delete_interest(request, interest_id):
    interest = get_object_or_404(Interest, id=interest_id)
    interest.delete()
    return redirect('edit_profile')


def search(request):
    try:
        context = {}
        context['search_text'] = request.POST.get('search_text')
        context['search_result'] = search_post(Post, context['search_text'])
        return render(request, 'search_result.html', context=context)
    except ValueError:
        return HttpResponseBadRequest('no search text')


@login_required
def follow(request, user_id):
    user = follow_controller(request, user_id)

    return redirect('profile', username=user.username)


def handle_404(request, exception):
    return render(request, '404.html')


def handle_500(request, exception):
    return render(request, '500.html')