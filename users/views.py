from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm, EmailAuthenticationForm


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = EmailAuthenticationForm
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    pass


class UserSignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:login')
