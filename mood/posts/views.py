from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from posts.models import Post

from .controllers import *


@login_required
def add_post(request):
    if request.method == 'POST':
        try:
            add_post_controller(request)
            return redirect('profile', username=request.user.username)
        except ValueError:
            return redirect('profile', username=request.user.username)

    else:
        return redirect('index')


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user_id == request.user.id:
        post.delete()
        return redirect('profile', username=request.user.username)
    else:
        return redirect('index') 
        

@login_required
def get_all_posts(request, username, index_page):
    context = {}
    try:
        all_posts = get_all_posts_controller(request, username, index_page)
        context['all_posts'] = all_posts['all_posts']
        context['profile'] = all_posts['profile']
        context['user'] = all_posts['user']
        
    except ValueError:
        return HttpResponseBadRequest('status code - 404')
    
    return render(request, 'all_posts.html', context=context)


@login_required
def get_feed(request, index_page):
    context = {}
    context['is_shuffle_feed'] = bool(request.GET.get('shuffle', False))
    context['all_posts'] = get_feed_controller(request, index_page, context['is_shuffle_feed'])
    print(context['all_posts'])
    
    return render(request, 'feed.html', context=context)


@login_required
def like_post(request, post_id):
    like_post_controller(request, post_id)


@login_required
def get_saved_posts(request):
    context = {}
    try:
        context['saved_posts'] = get_saved_posts_controller(request)
    except ValueError:
        context['saved_posts'] = []

    return render(request, 'saved.html', context=context)


def get_post(request, post_id):
    context = {}
    context['post'] = get_object_or_404(Post, id=post_id)
    return render(request, 'post_detail.html', context=context)