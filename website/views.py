from django.shortcuts import render,redirect
from django.contrib import messages
from dashboard.models import *
from website.models import *
from django.views.generic import View, TemplateView,CreateView
from.forms import *
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.core.mail import send_mail
from anidoso import settings
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required

# Create your views here.
class EcomMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get('cart_id')                
        print("dispatch")

        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            if request.user.is_authenticated:
                cart_obj.user = request.user
                cart_obj.save()
        return super().dispatch(request, *args, **kwargs)

# ******************* LANDING PAGE  VIEW *****************************
def home(request):
    product = Product.objects.all().order_by('-id')
    context = {
        'product':product
    }
    return render(request, 'website/home.html',context)

# ******************* PRODUCT CATEGORY VIEW *****************************
def category(request):
    category = Category.objects.all()
    context ={
        'category':category
    }
    return render(request, 'website/cat.html', context)

# ******************* CATEGORY RELATED PRODUCT VIEW *****************************
def collection(request, slug):
    if(Category.objects.filter(slug=slug)):
        product = Product.objects.filter(category__slug=slug)
        category_name = Category.objects.filter(slug=slug).first()
        context = {
            'product':product,
            'category_name':category_name
        }
    else:
        messages.warning(request, 'no such category exist')
    return render(request, 'website/cat_filter.html',context)

# ******************* PRODUCT DETAILS VIEW *****************************
def product_details(request,pk):
    product = Product.objects.get(id=pk)
    reviews = Review.objects.filter(product=product)
    context = {
        'product':product,
        'reviews': reviews
    }
    return render(request, 'website/product_detail.html',context)

# ******************* ADD TO CART VIEW *****************************
class AddToCartView(View):
    template_name = "website/add_to_cart.html"
    def get(self,request,pro_id):
        # get product
        product_obj = Product.objects.get(id=pro_id)
        # check if cart exists
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(
                product=product_obj)

            # item already exists in cart
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.selling_price
                cartproduct.save()
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
            # new item is added in cart
            else:
                cartproduct = CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price)
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
                return redirect('website-home')
        else:
            cart_obj = Cart.objects.create(total=0)
            request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(
                cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price)
            cart_obj.total += product_obj.selling_price
            cart_obj.save()
        
        if request.user.is_authenticated:
            cart_obj.customer = request.user
            cart_obj.save()
        return redirect('website-home')
        
        
# ******************* MANAGE CART  VIEW *****************************
class ManageCartView(View):

    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs['cp_id']
        action = request.GET.get('action')
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart

        if action == 'inc':
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()
        elif action == 'dcr':
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()
        elif action == 'rmv':
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect('mycart')

# ******************* CART VIEW *****************************
class MyCartView(EcomMixin,TemplateView):
    template_name = 'website/my_cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context 

# ******************* EMPTY CART VIEW *****************************
class EmptyCartView(View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get('cart_id', None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()  
        return redirect('mycart') 

# ******************* CHECK-OUT VIEW *****************************
class CheckOutView(EcomMixin, CreateView):
    template_name = 'website/checkout.html'
    form_class = CheckoutForm
    success_url = reverse_lazy('order_success')
    
    def dispatch(self, request, *args, **kwargs): 
        if request.user.is_authenticated:
            pass
        else:
            return redirect('/user/?next=/checkout/"')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total
            form.instance.order_status = "Order Received"
            name = form.cleaned_data.get('ordered_by')
            email = form.cleaned_data.get('email')
            # sending email to corresponding email.
            subject = "Order Received"
            message = "hello" + " " + name + " !! \n" + " We have received your order(s) \n" + "Our agent will contact you soon for delivery \n" + " Thank You !!"
            from_email = settings.EMAIL_HOST_USER
            to_list = [email]
            send_mail(subject, message, from_email, to_list, fail_silently=True)
            del self.request.session['cart_id']
        else:
            return redirect('website-home')
        return super().form_valid(form)

# ******************* BLOG VIEW *****************************
def blog(request):
    posts = Blog.objects.all().order_by('-id')
    context = {
        'posts':posts
    }
    return render(request,'website/blogs.html',context)

# ******************* ABOUT VIEW *****************************
def about(request):
    testimonies = Testimony.objects.all().order_by('id')
    about = About.objects.first()
    context = {
        'testimonies': testimonies,
        'about': about
    }
    return render(request,'website/about.html', context)

# ******************* CONTACT US VIEW *****************************
def contact(request):
    return render(request,'website/contact.html')

# ******************* RECEIVE CONTACT US INFO VIEW *****************************
def send(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Message successfully sent")
        return redirect('contact')
    else:
        for field, error in form.errors.items():
            error = strip_tags(error)
            messages.error(request,f"{field}: {error}")
            return redirect('contact')

# ******************* SEARCH PRODUCT VIEW *****************************
def search(request):
    if request.method == 'GET':
        kw = request.GET['keyword']
        result = Product.objects.filter(Q(title__icontains=kw) | Q(description__icontains=kw))
        context = {
            'result':result
        }
    return render(request,'website/search.html',context)

# ******************* ORDER SUCCESSFULL VIEW *****************************
@login_required(login_url="user-login")   
def order_success(request):

    return render(request, 'website/success.html')

# ******************* PRODUCT REVIEW VIEW *****************************
def review(request):
    if request.method == 'POST':
        pro_id = request.POST['pro_id']
        product = Product.objects.get(id=pro_id)
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.instance.product = product
            form.save()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = ReviewForm()
        for field, error in form.errors.items():
            error = strip_tags(error)
            messages.error(request,f"{field}: {error}")
            return redirect(request.META.get('HTTP_REFERER'))

    