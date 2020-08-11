from django.urls import path
from .views import signUp
from django.contrib.auth import views as auth_views
urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name='login.html'), name="login"),
    path("signup/", signUp, name='signup'),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
