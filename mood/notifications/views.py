from django.shortcuts import render
from django.contrib.auth.decorators import login_required   

from .models import Notification


@login_required
def get_notifications(request):
    context = {}
    context['notifications'] = Notification.objects.filter(user=request.user).all()
    return render(request, 'notifications.html', context=context)
