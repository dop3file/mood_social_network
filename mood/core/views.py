from django.shortcuts import render


def get_main_page(request):
    return render(request, 'index.html')

def register(request):
    return render(request, 'register.html')