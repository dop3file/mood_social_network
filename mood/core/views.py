from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from .forms import RegiserUserForm


def get_main_page(request):
    return render(request, 'index.html')


class RegisterUser(CreateView):
    form_class = RegiserUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))