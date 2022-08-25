from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from .forms import PostForm
from posts.models import Post
from core.models import Profile


def add_post(request):
    if request.method == 'POST':
        try:
            post_form = PostForm(instance=request.user, data=request.POST, files=request.FILES)
            if post_form.is_valid():
                post = Post(
                    user=request.user, 
                    text=post_form.cleaned_data['text'], 
                    image=post_form.cleaned_data['image'], 
                    type_mood=False if post_form.cleaned_data['type_mood'] == 'Белый' else True)
                post.save()
            return redirect('profile', username=request.user.username)
        except ValueError:
            return redirect('profile', username=request.user.username)

    else:
        return redirect('index')


def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user_id == request.user.id:
        post.delete()
        return redirect('profile', username=request.user.username)
    else:
        return redirect('index') 
        

def get_all_posts(request, username, index_page):
    context = {}
    try:
        context['all_posts'] = Paginator(Post.objects.filter(user__username=username).order_by('-date_post').all(), 5).page(index_page)
        context['profile'] = Profile.objects.get(user__username=username)
        context['user'] = context['profile'].user
        
    except ObjectDoesNotExist:
        return HttpResponseBadRequest('status code - 404')
    
    return render(request, 'all_posts.html', context=context)


def get_feed(request, index_page):
    context = {}
    context['all_posts'] = Paginator(Post.objects.exclude(user__username=request.user.username).order_by('-date_post').all(), 10).page(index_page)
    return render(request, 'feed.html', context=context)


def like_post(request, post_id):
    try:
        post = get_object_or_404(Post, id=post_id)
        if post.user.id == request.user.id:
            return redirect('index')
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        next = request.POST.get('next', '/')
        return redirect(next)
    except TypeError:
        next = request.POST.get('next', '/')
        return redirect(next)
