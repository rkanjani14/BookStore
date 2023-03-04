import json
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt

from .models import *
import razorpay
from django.conf import settings
from bookservices.constants import PaymentStatus
# Create your views here.

razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def home(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, "bookservices/home.html", context)


def sinup(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            try:
                user = User.objects.get(username=email)
                return render(request, 'bookservices/sinup.html', {"error": "User already Exist"})
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username=email, email=email, password=password1, first_name=first_name, last_name=last_name)
                customer = Customer.objects.create(user=user, phone=phone)
                auth.login(request, user)
                return redirect('/')
        else:
            return render(request, "bookservices/sinup.html", {"error": "password is not matched"})
    else:
        return render(request, "bookservices/sinup.html")


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request, "bookservices/login.html", {"error": "User Invalid"})
    else:
        return render(request, 'bookservices/login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def cart(request):
    user_name = request.user.username
    user = User.objects.get(username=user_name)
    print("user11", user)
    customer = Customer.objects.get(user=user)
    order, created = Order.objects.get_or_create(customer=customer, complete=PaymentStatus.PENDING)
    total_amount_cart = order.total_amount_cart
    total_number_cart = order.total_number_cart
    order_items = order.orderitem_set.all()
    context = {"order_items": order_items, "total_amount_cart": total_amount_cart,
               "total_number_cart": total_number_cart}
    return render(request, "bookservices/cart.html", context)


def update_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        book_id = data['bookId']
        action = data['action']
        try:
            cart_number = int(data['cartNumber'])
        except:
            cart_number = data['cartNumber']

        customer = Customer.objects.get(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=PaymentStatus.PENDING)
        book = Book.objects.get(id=book_id)
        order_item, created = OrderItem.objects.get_or_create(order=order, book=book)

        if action is None:
            if cart_number > 0:
                order_item.quantity = cart_number
                order_item.save()
            else:
                order_item.delete()

        if cart_number is None:
            if order_item.quantity >= 1:
                order_item.quantity += 1
            else:
                order_item.quantity = 1
            order_item.save()

    return JsonResponse("updated", safe=False)


def checkout(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        address = request.POST['address']
        country = request.POST['country']
        state = request.POST['state']
        city = request.POST['city']
        zip = request.POST['zip']

        customer = Customer.objects.get(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=PaymentStatus.PENDING)
        try:
            shipping_address = ShippingAddress.objects.get(customer=customer, order=order)
            shipping_address.first_name = first_name
            shipping_address.last_name = last_name
            shipping_address.address = address
            shipping_address.country = country
            shipping_address.state = state
            shipping_address.city = city
            shipping_address.zip = zip
            shipping_address.save()

        except:
            shipping_address = ShippingAddress.objects.create(customer=customer, order=order, first_name=first_name,
                                                              last_name=last_name, address=address, country=country,
                                                              state=state, city=city, zip=zip)
        cart_items = order.orderitem_set.all()
        total_amount_cart = order.total_amount_cart
        total_number_cart = order.total_number_cart
        order.paid = 0
        currency = "INR"
        amount = int(total_amount_cart * 100)
        if order.razorpay_order_id != "":
            razorpay_order = razorpay_client.order.fetch(order_id=order.razorpay_order_id)
        else:
            razorpay_order = razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture='0'))
            order.razorpay_order_id = razorpay_order['id']
            order.save()

        callback_url='/callback_url'
        context = {
            "razorpay_order_id": razorpay_order['id'],
            "razorpay_key_id": settings.RAZOR_KEY_ID,
            "currency": currency,
            "amount": amount,
            "callback_url": callback_url
        }
        return render(request, "bookservices/payment.html", context)

    customer = Customer.objects.get(user=request.user)
    order, created = Order.objects.get_or_create(customer=customer, complete=PaymentStatus.PENDING)
    cart_items = order.orderitem_set.all()
    total_amount_cart = order.total_amount_cart
    order.dues = total_amount_cart
    order.save()
    total_number_cart = order.total_number_cart


    context = {
        "cart_items": cart_items,
        "total_amount_cart": total_amount_cart,
        "total_number_cart": total_number_cart,
    }
    return render(request, "bookservices/checkout.html", context)


@csrf_exempt
def callback_url(request):
    if request.method == "POST":
        if "razorpay_signature" in request.POST:
            razorpay_payment_id = request.POST.get("razorpay_payment_id", "")
            razorpay_order_id = request.POST.get("razorpay_order_id", "")
            razorpay_signature = request.POST.get("razorpay_signature", "")
            order = Order.objects.get(razorpay_order_id=razorpay_order_id)
            order.razorpay_payment_id = razorpay_payment_id
            order.razorpay_signature = razorpay_signature
            amount = order.total_amount_cart
            order.paid = amount
            order.dues = 0
            params_dict = {
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_order_id": razorpay_order_id,
                "razorpay_signature": razorpay_signature
            }
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is not None:
                amount = int(amount * 100)
                razorpay_client.payment.capture(razorpay_payment_id, amount)
                order.complete = PaymentStatus.SUCCESS
                order.save()
                return render(request, 'bookservices/success.html')
            else:
                order.complete = PaymentStatus.FAILURE
                order.save()
                return render(request, "bookservices/failure.html")
        else:
            razorpay_payment_id = json.loads(request.body)['payment_id']
            razorpay_order_id = json.loads(request.body)['order_id']
            order = Order.objects.get(razorpay_order_id=razorpay_order_id)
            order.razorpay_payment_id = razorpay_payment_id
            order.complete = PaymentStatus.FAILURE
            order.save()
            return render(request, "bookservices/failure.html")