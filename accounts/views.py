# accounts/views.py
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.shortcuts import redirect

from .models import CustomUser
from .forms import CustomUserCreationForm, UserUpdateForm


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["welcome_message"] = "Welcome to Django CBV Home Page!"
        return context


class SignupView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:login")


class UserLoginView(LoginView):
    template_name = "accounts/login.html"


class UserLogoutView(LogoutView):
    template_name = "accounts/logged_out.html"
    next_page = reverse_lazy("accounts:login")


def user_logout(request):
    logout(request)
    return redirect("/")


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserUpdateForm
    template_name = "accounts/user_update.html"
    success_url = reverse_lazy("accounts:user_update")

    def get_object(self):
        return self.request.user


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = "accounts/user_confirm_delete.html"
    success_url = reverse_lazy("accounts:signup")

    def get_object(self):
        return self.request.user
