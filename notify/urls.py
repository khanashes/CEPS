from django.urls import path
from .views import notifyView, markReadView
urlpatterns = [
    path('',notifyView, name="notificationView"),
    path('markread/<int:id>/',markReadView, name="markRead")
]
