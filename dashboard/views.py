from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from django.contrib.auth.models import User
from .forms import ProductForm,CategoryForm
from django.views.generic import View, DetailView
from django.urls import reverse_lazy, reverse

# Create your views here.

# DASHBOARD FUNCTION
#@login_required(login_url='user-login')
def index(request):
    return render(request, "dashboard/index.html")

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

def category(request):
    if request.method =='POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.META.get("HTTP_REFERER"))
    else:
        form = CategoryForm()
    context = {
        'form':form
    }
    return render(request, "dashboard/category.html",context)

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

def new_orders(request):
    new_orders = Order.objects.filter(order_status="Order Received").order_by("-id")
    context = {
        'new_orders':new_orders
    }
    return render(request,"dashboard/new_order.html",context )

def user(request):
    return render(request, "dashboard/user.html")

def profile(request):
    return render(request, "dashboard/profile.html")

def subscriber(request):
    return render(request, "dashboard/subscriber.html")

