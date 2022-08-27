from django.shortcuts import get_object_or_404, redirect
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime
from collections import Counter

from posts.models import Post
from .models import Profile, Interest
from posts.forms import PostForm
from .forms import EditProfileForm

from notifications.controllers import follow_notification


def main_page_controller(request):
    context = {}
    hour = datetime.now().hour
    if 13 > hour >= 6 :
        context['welcome_msg'] = 'Доброе утро'
    elif 18 > hour >= 13:
        context['welcome_msg'] = 'Добрый день'
    else:
        context['welcome_msg'] = 'Добрый вечер'
    context['top_popular_posts'] = Counter([Post.objects.get(id=post.post_id) for post in Post.likes.through.objects.annotate(Count('post_id')).order_by('-post_id__count')[:5]])

    return context


def get_profile_controller(request, username):
    context = {}
    context['user'] = get_object_or_404(User, username=username)
    context['profile'] = Profile.objects.filter(user__username=username).first()
    context['interests'] = Interest.objects.filter(user=context['profile']).all()
    if request.user.username == username:
        context['post_form'] = PostForm()
    else:
        context['self_profile'] = get_object_or_404(Profile, user=request.user)
        context['is_follow'] = True if context['self_profile'] in context['user'].subscribers.all() else False

    context['posts'] = Post.objects.filter(user_id=User.objects.get(username=username).id).order_by('-date_post').all()[:5]
    

    return context


def edit_user_profile_controller(request, context):
    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        profile = Profile(user=request.user)

    form = EditProfileForm(instance=profile, data=request.POST, files=request.FILES)
    if form.is_valid():
        if form.cleaned_data['interest'] and len(context['interests']) != 3:
            interest = Interest(title=form.cleaned_data['interest'], user=profile)
            interest.save()
        form.save()


def follow_controller(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=request.user)
    if request.user.id == user_id:
        return redirect('index')
    if profile in user.subscribers.all():
        user.subscribers.remove(profile)
    else:
        user.subscribers.add(profile)
        follow_notification(request, user)
    

    return user


