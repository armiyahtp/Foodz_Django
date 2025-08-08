from django.urls import path
from api.v1.customer import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('account/', views.account, name='account'),



    path('address/', views.address, name='address'),
    path('address/add/', views.address_add, name='address_add'),
    path('address/edit/<int:id>/', views.address_update, name='address_update'),
    path('address/delete/<int:id>/', views.address_delete, name='address_delete'),



    path('slider/', views.slider, name='slider'),
    path('store/', views.store, name='store'),
    path('store/category/', views.store_category, name='store_category'),
    path('food/category/', views.food_category, name='food_category'),
    path('food/items/', views.food_items, name='food_items'),



    path('single/rest/<int:id>/', views.single_rest, name='single_rest'),
    path('cart/', views.cart, name='cart'),
    path('offer/', views.offer, name='offer'),
    path('order/', views.order, name='order'),
    path('order/item/', views.order_item, name='order_item'),
]