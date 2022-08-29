from multiprocessing.sharedctypes import Value
from django.shortcuts import redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage
from django.core.paginator import Paginator

from posts.models import Post
from core.models import Profile
from .forms import PostForm

from notifications.controllers import like_notification


def get_saved_posts_controller(request):
    try:
        saved_posts = [Post.objects.get(id=post.post_id) for post in Post.likes.through.objects.filter(user_id=request.user.id)]
        saved_posts.reverse()
    except ObjectDoesNotExist:
        raise ValueError

    return saved_posts


def like_post_controller(request, post_id: int):
    post = get_object_or_404(Post, id=post_id)
    if post.user.id == request.user.id:
        return redirect('index')
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        like_notification(request, post.user, post)
        


def get_feed_controller(request, index_page: int):
    feed = Paginator(Post.objects.exclude(user__username=request.user.username).exclude(likes=request.user).order_by('-date_post').all(), 10).page(index_page)
    return feed


def get_all_posts_controller(request, username: str, index_page: int):
    context = {}
    try:
        context['all_posts'] = Paginator(Post.objects.filter(user__username=username).order_by('-date_post').all(), 5).page(index_page)
        context['profile'] = Profile.objects.get(user__username=username)
        context['user'] = context['profile'].user
    except (ObjectDoesNotExist, EmptyPage):
        raise ValueError

    return context


def add_post_controller(request):
    try:
        post_form = PostForm(instance=request.user, data=request.POST, files=request.FILES)
        if post_form.is_valid():
            post = Post(
                user=request.user, 
                text=post_form.cleaned_data['text'], 
                image=post_form.cleaned_data['image'], 
                type_mood=False if post_form.cleaned_data['type_mood'] == 'Белый' else True)
            post.save()
    except ValueError:
        raise ValueError