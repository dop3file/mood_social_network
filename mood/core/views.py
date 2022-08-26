from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseBadRequest
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from .forms import RegiserUserForm, LoginUserForm, EditProfileForm
from django.contrib.auth.decorators import login_required   
from .models import Profile, Interest
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from posts.forms import PostForm
from posts.models import Post
from .utils import search_post, generate_default_avatar

from datetime import datetime
from collections import Counter


def get_main_page(request):
    context = {}
    hour = datetime.now().hour
    if 13 > hour >= 6 :
        context['welcome_msg'] = 'Доброе утро'
    elif 18 > hour >= 13:
        context['welcome_msg'] = 'Добрый день'
    else:
        context['welcome_msg'] = 'Добрый вечер'
    context['top_popular_posts'] = Counter([Post.objects.get(id=post.post_id) for post in Post.likes.through.objects.annotate(Count('post_id')).order_by('-post_id__count')[:5]])

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
    context = {}
    context['user'] = get_object_or_404(User, username=username)
    context['profile'] = Profile.objects.filter(user__username=username).first()
    context['interests'] = Interest.objects.filter(user_id=context['user'].id).all()
    if request.user.username == username:
        context['post_form'] = PostForm()

    context['posts'] = Post.objects.filter(user_id=User.objects.get(username=username).id).order_by('-date_post').all()[:5]

    return render(request, 'profile.html', context=context)
    

@login_required
def edit_user_profile(request):
    context = {}
    context['interests'] = Interest.objects.filter(user_id=request.user.id).all()

    if request.method == "POST":
        try:
            profile = Profile.objects.get(user=request.user)
        except ObjectDoesNotExist:
            profile = Profile(user=request.user)

        try:
            form = EditProfileForm(instance=profile, data=request.POST, files=request.FILES)
            if form.is_valid():
                if form.cleaned_data['interest'] and len(context['interests']) != 3:
                    interest = Interest(title=form.cleaned_data['interest'], user_id=request.user.id)
                    interest.save()
                form.save()
                return redirect('profile', username=request.user.username)
        except ValueError:
            messages.error(request, 'Попробуйте ещё раз')
            

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


def follow(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=request.user)
    if request.user.id == user_id:
        return redirect('index')
    if profile in user.subscribers.all():
        user.subscribers.remove(profile)
    else:
        user.subscribers.add(profile)

    return redirect('profile', username=user.username)