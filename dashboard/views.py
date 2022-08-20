from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from website.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import ProductForm,CategoryForm,BlogForm
from django.views.generic import View, DetailView
from django.urls import reverse_lazy, reverse

# Create your views here.

# DASHBOARD FUNCTION
@login_required(login_url="admin_login")   
def index(request):
    return render(request, "dashboard/index.html")

@login_required(login_url="admin_login")   
def product(request):
    products = Product.objects.all().order_by('-id')
    if request.method =='POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            product_name  = form.cleaned_data.get('title')
            messages.success(request,f'{product_name} has been added')
            return redirect(request.META.get("HTTP_REFERER"))
    else:
        form = ProductForm()
    context = {
        'form':form,
        'products':products
    }
    return render(request, "dashboard/product.html", context)

@login_required(login_url="admin_login")   
def category(request):
    if request.method =='POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            cat_name  = form.cleaned_data.get('title')
            messages.success(request,f'{cat_name} category added')
            return redirect(request.META.get("HTTP_REFERER"))
    else:
        form = CategoryForm()
    context = {
        'form':form
    }
    return render(request, "dashboard/category.html",context)

@login_required(login_url="admin_login")   
def edit_product(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('dashboard-product')
    else:
        form = ProductForm(instance=product)
    context = {
        'form': form
    }
    return render(request, "dashboard/edit_product.html", context)

@login_required(login_url="admin_login")   
def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'product deleted successfully')
        return redirect('dashboard-product')
    context = {
        'product': product
    }
    return render(request, "dashboard/delete_product.html", context)

@login_required(login_url="admin_login")   
def order(request):
    orders = Order.objects.all().order_by('id')
    context = {
        'orders':orders
    }
    return render(request, "dashboard/order.html", context)

class AdminOrderDetailView(DetailView):
    template_name = 'dashboard/order_detail.html'
    model = Order
    context_object_name = 'ord_obj'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["allstatus"] = ORDER_STATUS
        return context

    
class OrderStatusChangeView(View):
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs['pk']
        order_obj = Order.objects.get(id=order_id)
        new_status = request.POST.get('status')
        order_obj.order_status = new_status
        order_obj.save()
        return redirect(reverse_lazy('dashboard-order-detail', kwargs={'pk': order_id}))

@login_required(login_url="admin_login")   
def new_orders(request):
    new_orders = Order.objects.filter(order_status="Order Received").order_by("-id")
    context = {
        'new_orders':new_orders
    }
    return render(request,"dashboard/new_order.html",context )

@login_required(login_url="admin_login")   
def user(request):
    customers = User.objects.all()
    context = {
        'customers': customers
    }
    return render(request, "dashboard/user.html",context)

@login_required(login_url="admin_login")   
def profile(request,pk):
    customer = User.objects.get(id=pk)
    context = {
        'customer': customer
    }
    return render(request, "dashboard/profile.html",context)


def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None and user.is_staff and user.is_superuser:
            login(request, user)
            return redirect('dashboard-index')

        else:
            messages.error(request, "Invalid Credential")
            return redirect("admin_login")

    return render(request, 'dashboard/admin_login.html')

def log_out(request):
    logout(request)
    messages.success(request, "You have successfully logged out")
    return redirect("admin_login")

def success(request):
    return render(request, 'dashboard/password_change_success.html')


@login_required(login_url="admin_login")   
def post(request):
    if request.method =='POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,' blog posted successfully')
            return redirect(request.META.get("HTTP_REFERER"))
    else:
        form = BlogForm()
    context = {
        'form':form
    }
    return render(request, "dashboard/blog.html", context)

@login_required(login_url="admin_login")   
def message(request):
    messages = Contact.objects.all().order_by('-id')
    context = {
        'messages': messages
    }
    return render(request, 'dashboard/message.html',context)

def del_message(request, pk):
    mgs = Contact.objects.get(id=pk)
    if request.method == 'POST':
        mgs.delete()
        return redirect('dashboard-message')
    context = {
        'mgs': mgs
    }
    return render(request, 'dashboard/del_message.html',context)