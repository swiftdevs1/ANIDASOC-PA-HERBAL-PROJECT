from django.shortcuts import render,redirect
from django.views.generic import View, CreateView, FormView,DetailView
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from dashboard.models import *
from .forms import *

# Create your views here.
# ******************* REGISTER VIEW *****************************
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']

        if User.objects.filter(username=username):
            messages.error(request, "Username Already Exist")
            return redirect("register")

        if User.objects.filter(email=email):
            messages.error(request, "Email Already Exist")
            return redirect("register")

        if len(username)< 4:
            messages.error(request, "Username must be atleast 4 characters")
            return redirect("register")

        if not password.isalnum():
            messages.error(request, "password must be Alph-Numeric")
            return redirect("register")

        if password != password1:
            messages.error(request, "Password do not match")
            return redirect("register")


        myuser = User.objects.create_user(username, email, password)
        myuser.save()
        
        messages.success(request, "Your account has been successfully created")
        return redirect("user-login")
    
    return render(request,'user/register.html')


# ******************* LOGIN VIEW *****************************
def sign_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None :
            login(request, user)
            return redirect('website-home')

        else:
            messages.error(request, "Invalid Credential")
            return redirect("user-login")
    return render(request,'user/login.html')

# ******************* LOG-OUT VIEW *****************************
def sign_out(request):
    logout(request)
    return redirect("website-home")

# ******************* PROFILE VIEW *****************************
@login_required(login_url="user-login")   
def profile(request):
    return render(request, 'user/profile.html')

# ******************* PROFILE UPDATE VIEW *****************************
@login_required(login_url="user-login")   
def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile successfully updated")
            return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'user/profile_update.html',context)

# ******************* USER DASHBOARD  VIEW *****************************
@login_required(login_url="user-login")   
def user_home(request):
    user = request.user
    orders = Order.objects.filter(cart__customer=user).order_by('id')
    context = {
        'orders': orders
    }
    return render(request, 'user/home.html', context)
    
# ******************* USER SETTING VIEW *****************************
@login_required(login_url="user-login")   
def setting(request):
    if request.method == 'POST':
        current  = request.POST['current']
        new  = request.POST['new']
        new1  = request.POST['new1']
        if new != new1:
            messages.error(request, "Password do not match")
            return redirect(request.META.get("HTTP_REFERER"))
        user = authenticate(username=request.user.username,password=current)
        if(user):
            user.set_password(new)
            user.save()
            messages.success(request, "Password changed successfully")
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.error(request, "incorrect curent password")
            return redirect(request.META.get("HTTP_REFERER"))

    return render(request, 'user/settings.html')


# ******************* USER ORDER DETAILS VIEW *****************************
class CustomerOrderDetail(DetailView):
    template_name = 'user/user_order_detail.html'
    model = Order
    context_object_name = 'ord_obj'
