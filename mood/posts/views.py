from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required   
from .forms import PostForm
from posts.models import Post


@login_required
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
    post = Post.objects.get(id=post_id)
    if post.user_id == request.user.id:
        post.delete()
        return redirect('profile', username=request.user.username)
    else:
        return redirect('index') 
        
