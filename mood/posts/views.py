from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from .forms import PostForm
from .models import Post


def add_post(request):
    if request.method == 'POST':

        post_form = PostForm(instance=request.user, data=request.POST, files=request.FILES)
        if post_form.is_valid():
            post = Post(
                user=request.user, 
                text=post_form.cleaned_data['text'], 
                image=post_form.cleaned_data['image'], 
                type_mood=False if post_form.cleaned_data['type_mood'] == '1' else True)
            post.save()
            return redirect('profile', username=request.user.username)
        else:
            return redirect('profile', username=request.user.username)

    else:
        return redirect('index')
        
