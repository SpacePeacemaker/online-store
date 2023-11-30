from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

from .forms import MyUserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView
from .forms import UserLoginForm
from django.contrib.auth.mixins import LoginRequiredMixin


class MyRegisterView(CreateView):
    """Регистрация пользователя"""

    form_class = MyUserCreationForm
    template_name = "accounts/registration.jinja2"
    success_url = reverse_lazy("accounts:my-account")

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse("accounts:my-account"))
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")
        user = authenticate(self.request, email=email, password=password)
        login(request=self.request, user=user)
        return response


class MyAccountView(LoginRequiredMixin, TemplateView):
    """Личный кабинет пользователя"""

    template_name = "accounts/my-account.jinja2"
    login_url = "/login/"


class MyLoginView(LoginView):
    """Класс представления для входа пользователя"""

    template_name = "accounts/login.jinja2"
    authentication_form = UserLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        previous_page = self.request.GET.get("next") if self.request.GET.get("next") is not None else "/"
        next_page = previous_page
        return next_page


class MyLogoutView(LogoutView):
    """Класс представления для выхода пользователя"""

    next_page = reverse_lazy("shops:home")
