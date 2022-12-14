from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, PasswordChangeForm , CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator




class Productview(View):
 def get(self, request):
  football = Product.objects.filter(category='F')
  cricket = Product.objects.filter(category='C')
  return render(request, 'app/home.html', { 'football': football,'cricket' : cricket})


class ProductDeatilView(View):
 def get(self, request, pk):
  product = Product.objects.get(pk=pk)
  item_already_in_cart = False
  if request.user.is_authenticated:
    item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
  return render(request, 'app/productdetail.html', {'product': product, 'item_already_in_cart':item_already_in_cart})

@login_required
def add_to_cart(request):
 user=request.user
 product_id=request.GET.get('prod_id')
 product=Product.objects.get(id=product_id)
 Cart(user = user, product=product).save()
 return redirect('/cart')

@login_required
def show_cart(request):
 if request.user.is_authenticated:
  user = request.user
  cart = Cart.objects.filter(user=user)
  amount = 0.0
  shiiping_amount = 60.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == user]
  if cart_product:
   for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount
    total_amount = amount + shiiping_amount
   return render(request, 'app/addtocart.html', {'cart': cart, 'totalamount': total_amount, 'amount': amount, 'shipingamount': shiiping_amount})
  else:
   return render(request, 'app/emptycart.html')

def plus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get( Q (product = prod_id) & Q (user=request.user))
  c.quantity += 1
  c.save()
  amount = 0.0
  shiiping_amount = 60.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user ==request.user]
  if cart_product:
   for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount
    total_amount = amount + shiiping_amount
  data = {
     'quantity': c.quantity,
     'amount': amount,
     'totalamount': total_amount
    }
  return JsonResponse(data)

def minus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get( Q (product = prod_id) & Q (user=request.user))
  c.quantity -= 1
  c.save()
  amount = 0.0
  shiiping_amount = 60.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user ==request.user]
  if cart_product:
   for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount
    total_amount = amount + shiiping_amount
  data = {
     'quantity': c.quantity,
     'amount': amount,
     'totalamount': total_amount
    }
  return JsonResponse(data)

def remove_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get( Q (product = prod_id) & Q (user=request.user))

  c.delete()
  amount = 0.0
  shiiping_amount = 60.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user ==request.user]
  if cart_product:
   for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount
    total_amount = amount + shiiping_amount
  data = {
     'amount': amount,
     'totalamount': total_amount
    }
  return JsonResponse(data)


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
 def get(self, request):
  form = CustomerProfileForm()
  return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})
 def post(self, request):
  form = CustomerProfileForm(request.POST)
  if form.is_valid():
   usr = request.user
   name = form.cleaned_data['name']
   phone_no = form.cleaned_data['phone_no']
   email = form.cleaned_data['email']
   address = form.cleaned_data['address']
   reg = Customer(user=usr, name=name, phone_no=phone_no,email=email,address=address)
   reg.save()
   messages.success(request, 'Congratulations!! Profile Update Successfully')
  return render(request, 'app/profile.html', {'form': form})

@login_required
def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html', {'add': add, 'active': 'btn-primary'})

@login_required
def orders(request):
  op = OrderPlaced.objects.filter(user = request.user)
  return render(request, 'app/orders.html', {'order_placed': op})

class change_password(View):
 def get(self, request):
  form=PasswordChangeForm()
  messages.success(request, 'Congratulations!! Changed Successfully')
  return render(request, 'app/changepassword.html', {'form': form})

def football(request, data = None):
 if data == None:
  football = Product.objects.filter(category='F')
  return render(request, 'app/football.html', {'footballs': football})

def cricket(request, data = None):
  # if data == None:
  cricket = Product.objects.filter(category='C')
  return render(request, 'app/cricket.html', {'crickets': cricket})


# def buynow(request):
#  return render(request, 'app/buy-now.html')

def contactus(request):
  return render(request, 'app/contact.html')

class CustomerRegistrationView(View):
 def get (self, request):
  form = CustomerRegistrationForm()
  return render(request, 'app/customerregistration.html', {'form': form})

 def post(self, request):
  form=CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request, 'Congratulations!! Registered Successfully')
   form.save()
  return render(request, 'app/customerregistration.html', {'form': form})

@login_required
def checkout(request):
  user = request.user
  add = Customer.objects.filter(user=user)
  cart_items = Cart.objects.filter(user = user)
  amount = 0.0
  shiiping_amount = 60.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user ==request.user]
  if cart_product:
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount
      total_amount = amount + shiiping_amount

  return render(request, 'app/checkout.html', {'add': add, 'totalamount': total_amount, 'cart_items': cart_items})

@login_required
def order_done(request):
  user = request.user
  custid = request.GET.get('custid')
  customer = Customer.objects.get(id = custid)
  cart = Cart.objects.filter(user = user)
  for c in cart:
    OrderPlaced(user=user, customer = customer, product=c.product, quantity = c.quantity).save()
    c.delete()
  return redirect("orders")


