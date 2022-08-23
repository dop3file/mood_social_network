from django.shortcuts import render, redirect
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
    try:
        post = Post.objects.get(id=post_id)
    except ObjectDoesNotExist:
        return HttpResponseBadRequest('status code - 404')
    if post.user_id == request.user.id:
        post.delete()
        return redirect('profile', username=request.user.username)
    else:
        return redirect('index') 
        

def get_all_posts(request, username, index_page):
    context = {}
    try:
        all_posts = Paginator(Post.objects.filter(user__username=username).order_by('-date_post').all(), 5)
        context['all_posts'] = all_posts.page(index_page)
        context['profile'] = Profile.objects.get(user__username=username)
        context['user'] = context['profile'].user
        
    except ObjectDoesNotExist:
        return HttpResponseBadRequest('status code - 404')
    
    return render(request, 'all_posts.html', context=context)
