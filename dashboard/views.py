from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from website.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import *
from django.views.generic import View, DetailView
from django.urls import reverse_lazy, reverse

# Create your views here.
# ******************* ADMIN DASHBOARD HOME VIEW *****************************
@login_required(login_url="admin_login")   
def index(request):
    products = Product.objects.all()
    orders = Order.objects.all()
    product_count = Product.objects.all().count()
    user_count = User.objects.all().count()
    cat_count = Category.objects.all().count()
    order_count = Order.objects.all().count()
    context = {
        'product_count': product_count,
        'user_count': user_count,
        'cat_count': cat_count,
        'order_count': order_count,
        'products': products,
        'orders': orders
    }
    
    return render(request, "dashboard/index.html",context)

# ******************* ADMIN ADD PRODUCT VIEW *****************************
@login_required(login_url="admin_login")   
def product(request):
    products = Product.objects.all().order_by('-id')
    product_count = Product.objects.all().count()
    user_count = User.objects.all().count()
    cat_count = Category.objects.all().count()
    order_count = Order.objects.all().count()
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
        'products':products,
        'product_count': product_count,
        'user_count': user_count,
        'cat_count': cat_count,
        'order_count': order_count
    }
    return render(request, "dashboard/product.html", context)

# ******************* ADMIN CREATE CATEGORY VIEW *****************************
@login_required(login_url="admin_login")   
def category(request):
    product_count = Product.objects.all().count()
    user_count = User.objects.all().count()
    cat_count = Category.objects.all().count()
    order_count = Order.objects.all().count()
    if request.method =='POST':
        form = CategoryForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            cat_name  = form.cleaned_data.get('title')
            messages.success(request,f'{cat_name} category added')
            return redirect(request.META.get("HTTP_REFERER"))
    else:
        form = CategoryForm()
    context = {
        'form':form,
        'product_count': product_count,
        'user_count': user_count,
        'cat_count': cat_count,
        'order_count': order_count
   
    }
    return render(request, "dashboard/category.html",context)

# ******************* ADMIN EDIT PRODUCT VIEW *****************************
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

# ******************* ADMIN DELETE PRODUCT VIEW *****************************
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

# ******************* ADMIN VIEW PRODUCT ORDER VIEW *****************************
@login_required(login_url="admin_login")   
def order(request):
    product_count = Product.objects.all().count()
    user_count = User.objects.all().count()
    cat_count = Category.objects.all().count()
    order_count = Order.objects.all().count()
    orders = Order.objects.all().order_by('id')
    context = {
        'orders':orders,
        'product_count': product_count,
        'user_count': user_count,
        'cat_count': cat_count,
        'order_count': order_count
   
    }
    return render(request, "dashboard/order.html", context)

# ******************* ADMIN VIEW FOR USER ORDER DETAILS VIEW *****************************
class AdminOrderDetailView(DetailView):
    template_name = 'dashboard/order_detail.html'
    model = Order
    context_object_name = 'ord_obj'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["allstatus"] = ORDER_STATUS
        return context

 # ******************* ADMIN VIEW FOR CHANGING ORDER STATUS  *****************************   
class OrderStatusChangeView(View):
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs['pk']
        order_obj = Order.objects.get(id=order_id)
        new_status = request.POST.get('status')
        order_obj.order_status = new_status
        order_obj.save()
        return redirect(reverse_lazy('dashboard-order-detail', kwargs={'pk': order_id}))

# ******************* ADMIN VIEW FOR NEW ORDERS  *****************************
@login_required(login_url="admin_login")   
def new_orders(request):
    new_orders = Order.objects.filter(order_status="Order Received").order_by("-id")
    context = {
        'new_orders':new_orders
    }
    return render(request,"dashboard/new_order.html",context )

# ******************* GETTING ALL USERS VIEW *****************************
@login_required(login_url="admin_login")   
def user(request):
    customers = User.objects.all()
    product_count = Product.objects.all().count()
    user_count = User.objects.all().count()
    cat_count = Category.objects.all().count()
    order_count = Order.objects.all().count()
    
    context = {
        'customers': customers,
        'product_count': product_count,
        'user_count': user_count,
        'cat_count': cat_count,
        'order_count': order_count
    }
    return render(request, "dashboard/user.html",context)

# ******************* GETTING EACH USER PROFILE VIEW *****************************
@login_required(login_url="admin_login")   
def profile_detail(request,pk):
    customer = User.objects.get(id=pk)
    context = {
        'customer': customer
    }
    return render(request, "dashboard/profile.html",context)

# ******************* ADMIN LOGIN AUTHENTICATION VIEW *****************************
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

# ******************* ADMIN LOG-OUT VIEW *****************************
def log_out(request):
    logout(request)
    messages.success(request, "You have successfully logged out")
    return redirect("admin_login")

# ******************* ADMIN CHANGE PASSWORD SUCCESS REDIRECTION VIEW *****************************
def success(request):
    return render(request, 'dashboard/password_change_success.html')

# ******************* ADMIN POST/ BLOG CREATION VIEW *****************************
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

# ******************* GETTING ALL MESSAGE FROM CONTACT US FORM *****************************
@login_required(login_url="admin_login")   
def message(request):
    messages = Contact.objects.all().order_by('-id')
    context = {
        'messages': messages
    }
    return render(request, 'dashboard/message.html',context)

# ******************* DELETE MESSAGE VIEW  *****************************
@login_required(login_url="admin_login")   
def del_message(request, pk):
    mgs = Contact.objects.get(id=pk)
    if request.method == 'POST':
        mgs.delete()
        return redirect('dashboard-message')
    context = {
        'mgs': mgs
    }
    return render(request, 'dashboard/del_message.html',context)

# ******************* ADD TESTIMONY VIEW *****************************
@login_required(login_url="admin_login")   
def testimony(request):
    if request.method == 'POST':
        test_form = TestimonyForm(request.POST, request.FILES)
        if test_form.is_valid():
            test_form.save()
            messages.success(request,' testimony added successfully')
            return redirect(request.META.get("HTTP_REFERER"))
    else:
        test_form = TestimonyForm()
    context = {
            'test_form': test_form
        }
    return render(request, 'dashboard/testimony.html', context)

# ******************* WRITE ABOUT US VIEW *****************************
@login_required(login_url="admin_login")   
def about_us(request):
    about = About.objects.all()
    if request.method == 'POST':
        about_form = AboutForm(request.POST)
        if about_form.is_valid():
            about_form.save()
            messages.success(request,' testimony added successfully')
            return redirect(request.META.get("HTTP_REFERER"))
    else:
        about_form = AboutForm()
    context = {
        'about_form': about_form,
        'about': about
    }
    return render(request, 'dashboard/about.html', context)

# ******************* EDIT ABOUT US VIEW *****************************   
@login_required(login_url="admin_login")   
def edit_about(request,pk):
    item = About.objects.get(id=pk)
    if request.method == 'POST':
        form  = AboutForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
    else:
        form = AboutForm(instance=item)
    context = {
        'form': form
    }
    return render(request, 'dashboard/edit_about.html', context)