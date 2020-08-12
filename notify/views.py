from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.models import User
from notifications.models import Notification

def notifyView(request):
    query = request.user.notifications.unread()
    return render(request, template_name='scraper/notificationView.html', context={'query':query})

def markReadView(request, id):
    query = Notification.objects.get(id=id)
    query.mark_as_read()
    return redirect('wishListView')