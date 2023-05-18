from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
import json
import datetime
from .models import Customer
from django.shortcuts import get_object_or_404, render

from .models import *
from . utils import cookieCart, cartData, guestOrder

from django.http import JsonResponse

#crear, registrar e iniciar sesion
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

# Create your views here.


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'store/product_detail.html', {'product': product})


def welcome(request):
    return render(request, 'store/welcome.html')


def store(request):

    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)


def checkoout(request):
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def updateItem(request):
    data = json.loads(request.body.decode('utf-8'))
    productId = data['productId']
    action = data['action']

    print('Action: ', action)
    print('productId: ', productId)


#    data = json.load(request.data)
#   productId = data['productId']
#    action = data['action']

#    print('Action: ', action)
#    print('productId: ', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)


    order, created = Order.objects.get_or_create(
    customer=customer, complete=False)

    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item agregado', safe=False)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        
    else:
        customer, order = guestOrder(request, data)
        
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            adress=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
            )

    return JsonResponse('Pago completado', safe=False)


#seccion login, signup

def signup(request):
    if request.method == 'GET':
        print('enviando formulario')
        return render(request, 'store/signup.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            # Registrar usuario
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                # Crear objeto Customer asociado al usuario
                customer, created = Customer.objects.get_or_create(user=user, defaults={'name': user.username})
                login(request, user)
                return redirect('store')
            except:
                return render(request, 'store/signup.html', {'form': UserCreationForm, 'error': 'Usuario ya existe'})
        return render(request, 'store/signup.html', {'form': UserCreationForm, 'error': 'Contraseña no coincide'})
    
def singout(request):
    logout(request)
    return redirect('welcome')

def signin(request):
    if request.method == 'GET':
        return render(request,'store/signin.html', {'form': AuthenticationForm})
    else:   
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            return render(request,'store/signin.html', {'form': AuthenticationForm, 'error': 'Usuario o contraseña incorrectos'})

#paypal

def create_paypal_order_view(request):
    if request.method == 'POST':
        # Lógica para crear la orden de PayPal
        return JsonResponse({'orderID': '...'})  # Retorna la respuesta como JSON

def capture_paypal_order_view(request):
    if request.method == 'POST':
        # Lógica para capturar la orden de PayPal
        return JsonResponse({'status': 'success'})  # Retorna la respuesta como JSON
