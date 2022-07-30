from django.shortcuts import render,redirect
from django.views.generic import View, CreateView, FormView
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy, reverse
from .models import *
from .forms import *

# Create your views here.
class CustomerRegistrationView(CreateView):
    template_name = "user/register.html"
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy("website-home")

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        user = User.objects.create_user(username, email, password)
        form.instance.user = user
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        if 'next' in self.request.GET:
            next_url = self.request.GET.get('next')
            return next_url
        else:
            return self.success_url

class CustomerLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('website-home')


class CustomerLoginView(FormView):
    template_name = "user/login.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("website-home")

# form_valid method is a type of post method available in CreateView, FormView and UpdateView
    def form_valid(self, form):
        uname = form.cleaned_data.get('username')
        pword = form.cleaned_data.get('password')
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Customer.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {'form': self.form_class, 'error': 'invalid credentials'})

        return super().form_valid(form)

    def get_success_url(self):
        if 'next' in self.request.GET:
            next_url = self.request.GET.get('next')
            return next_url
        else:
            return self.success_url

