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
from loguru import logger

from notifications.controllers import follow_notification


logger.add("out.log", backtrace=True)


@logger.catch
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
    context['top_popular_users'] = Counter(Profile.subscribers.through.objects.annotate(Count('user_id')).order_by('user_id__count')).most_common(5)
    context['admins'] = User.objects.filter(is_staff=True).all()

    return context


@logger.catch
def get_profile_controller(request, username):
    context = {}
    context['user'] = User.objects.filter(username=username).first()
    context['profile'] = Profile.objects.filter(user__username=username).first()
    context['interests'] = Interest.objects.filter(user=context['profile']).all()
    if request.user.username == username:
        context['post_form'] = PostForm()
    else:
        if request.user.is_authenticated:
            context['self_profile'] = Profile.objects.filter(user=request.user).first()
            context['is_follow'] = True if context['self_profile'] in context['user'].subscribers.all() else False

    context['posts'] = Post.objects.filter(user_id=User.objects.get(username=username).id).order_by('-date_post').all()[:5]
    

    return context


@logger.catch
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


@logger.catch
def follow_controller(request, user_id):
    user = get_object_or_404(User, id=user_id)
    self_profile = get_object_or_404(Profile, user=request.user)
    if request.user.id == user_id:
        return redirect('index')
    if self_profile in user.subscribers.all():
        user.subscribers.remove(self_profile)
    else:
        user.subscribers.add(self_profile)
        follow_notification(request, user)
    
    return user


