from django.shortcuts import render
from django.contrib.auth.decorators import login_required   

from .models import Notification
from .controllers import get_all_notifications


@login_required
def get_notifications(request):
    context = {}
    context['notifications'] = get_all_notifications(request)
    return render(request, 'notifications.html', context=context)
