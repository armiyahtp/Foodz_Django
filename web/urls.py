from django.urls import path
from web import views

app_name = "web"


urlpatterns = [
   path('', views.index, name="index"),
   path('login/', views.login, name="login"),
   path('register/', views.register, name="register"),
   path('logout/', views.logout, name="logout"),
   path('restaurants/<int:id>/', views.restaurants, name="restaurants"),
   
   path('single_restaurant/<int:id>/', views.single_restaurant, name="single_restaurant"),
   path('single_restaurant/cart_add/<int:id>/', views.cart_add, name="cart_add"),
   path('single_restaurant/rest_cart_plus/<int:id>/', views.rest_cart_plus, name="rest_cart_plus"),
   path('single_restaurant/rest_cart_minus/<int:id>/', views.rest_cart_minus, name="rest_cart_minus"),



   path('cart/', views.cart, name="cart"),
   path('cart/cart_plus/<int:id>/', views.cart_plus, name="cart_plus"),
   path('cart/cart_minus/<int:id>/', views.cart_minus, name="cart_minus"),


   path('offers/', views.offers, name="offers"),
   path('offer/apply/<int:id>', views.offer_apply, name="offer_apply"),


   path('checkout/', views.checkout, name="checkout"),
   path('account/', views.account, name="account"),


   path('address/', views.address, name="address"),
   path('add_address/', views.add_address, name="add_address"),
   path('address/edit/<int:id>', views.edit_address, name="edit_address"),
   path('address/delete/<int:id>', views.delete_address, name="delete_address"),
   path('address/select/<int:id>', views.select_address, name="select_address"),

   path('place_order/', views.place_order, name="place_order"),

   path('orders/', views.orders, name="orders"),
   path('order_tracking/<int:id>', views.order_tracking, name="order_tracking"),
]
