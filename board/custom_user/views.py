from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm


class SignUpView(CreateView):
    """Вью регистрации"""
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'custom_user/signup.html'


class MyLoginView(LoginView):
    """Вью логина"""
    template_name = 'custom_user/login.html'


class MyLogoutView(LogoutView):
    template_name = 'mysite/base_mysite.html'
