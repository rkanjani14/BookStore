from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('cart/', views.cart, name="cart"),
    path('update_cart/', views.update_cart, name="update_cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('callback_url', views.callback_url, name="callback_url"),
    path('sinup/', views.sinup, name="sinup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
]
