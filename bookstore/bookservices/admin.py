from django.contrib import admin
from bookservices.models import Customer, Author, Order, Book, OrderItem, ShippingAddress


# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'price', 'about_book', 'image')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'date', 'complete', 'paid', 'dues', 'razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'book', 'quantity')


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'customer', 'first_name', 'last_name', 'address', 'country', 'state', 'city', 'zip')
