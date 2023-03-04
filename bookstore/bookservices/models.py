from django.db import models
from django.contrib.auth.models import User
from bookservices.constants import PaymentStatus


# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField()

    def __str__(self):
        return self.user.username


class Author(models.Model):
    name = models.CharField(max_length=512)

    def __str__(self):
        return self.name


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=512, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    image = models.ImageField(upload_to='book/')
    about_book = models.TextField(null=True)

    def __str__(self):
        return self.title


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    complete = models.CharField(max_length=20, default=PaymentStatus.PENDING)
    date = models.DateTimeField(auto_now=True)
    paid = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    dues = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    razorpay_order_id = models.CharField(max_length=40, null=False , blank=False)
    razorpay_payment_id = models.CharField(max_length=36, null=False, blank=False)
    razorpay_signature = models.CharField(max_length=128, null=False, blank=False)

    def __str__(self):
        return str(self.id)

    @property
    def total_amount_cart(self):
        order_items = self.orderitem_set.all()
        total = sum([item.book.price * item.quantity for item in order_items])
        return total

    @property
    def total_number_cart(self):
        order_items = self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total


# class transaction(models.Model):
#     order = models.OneToOneField(Order, on_delete=models.SET_NULL, null=True)
#     status = models.CharField(default=PaymentStatus.PENDING, max_length=254, null=False, blank=False)
#     provider_order_id = models.CharField(max_length=40, null=False , blank=False)
#     payment_id = models.CharField(max_length=36, null=False, blank=False)
#     signature_id = models.CharField(max_length=128, null=False, blank=False)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return str(self.id)

    @property
    def one_item_total(self):
        total = self.book.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=512)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name + "  " + self.address
