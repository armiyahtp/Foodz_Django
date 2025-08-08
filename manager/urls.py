from django.urls import path
from manager import views

app_name = "manager"



urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('profile/',views.profile,name='profile'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),




    path('store_category/',views.store_category,name='store_category'),
    path('store_category_create/',views.store_category_create,name='store_category_create'),
    path('store_category_update/<int:id>/',views.store_category_update,name='store_category_update'),
    path('store_category_delete/<int:id>/',views.store_category_delete,name='store_category_delete'),



    path('store/',views.store,name='store'),
    path('single_store/<int:id>/',views.single_store,name='single_store'),
    path('store_create/',views.store_create,name='store_create'),
    path('store_update/<int:id>/',views.store_update,name='store_update'),
    path('store_delete/<int:id>/',views.store_delete,name='store_delete'),



    path('order/<int:id>/',views.order,name='order'),
    path('order/assign/<int:id>/',views.order_assign,name='order_assign'),
    path('order/accept/<int:id>/',views.order_accept,name='order_accept'),
    path('order/reject/<int:id>/',views.order_reject,name='order_reject'),
    path('order/prepared/<int:id>/',views.order_prepared,name='order_prepared'),
    path('order/picked/<int:id>/',views.order_picked,name='order_picked'),
    path('order/completed/<int:id>/',views.order_completed,name='order_completed'),
    path('order/delete/<int:id>/',views.order_delete,name='order_delete'),




    path('food_category/',views.food_category,name='food_category'),
    path('food_category_create/',views.food_category_create,name='food_category_create'),
    path('food_category_update/<int:id>/',views.food_category_update,name='food_category_update'),
    path('food_category_delete/<int:id>/',views.food_category_delete,name='food_category_delete'),




    path('food_item/',views.food_item,name='food_item'),
    path('food_item_create/',views.food_item_create,name='food_item_create'),
    path('single_food_item/<int:id>',views.single_food_item,name='single_food_item'),
    path('food_item_update/<int:id>/',views.food_item_update,name='food_item_update'),
    path('food_item_delete/<int:id>/',views.food_item_delete,name='food_item_delete'),

    


    path('slider/',views.slider,name='slider'),
    path('slider_create/',views.slider_create,name='slider_create'),
    path('slider_update/<int:id>/',views.slider_update,name='slider_update'),
    path('slider_delete/<int:id>/',views.slider_delete,name='slider_delete'),




    path('carts/',views.carts,name='carts'),
    path('carts/delete/<int:id>/',views.carts_delete,name='carts_delete'),



    path('order/item/',views.order_item,name='order_item'),
    path('order/item/delete/<int:id>/',views.order_item_delete,name='order_item_delete'),



    path('address/',views.address,name='address'),
    path('address/<int:id>/',views.address_delete,name='address_delete'),




    path('offer/',views.offer,name='offer'),
    path('offer/create/',views.offer_create,name='offer_create'),
    path('offer/update/<int:id>/',views.offer_update,name='offer_update'),
    path('offer/delete/<int:id>/',views.offer_delete,name='offer_delete'),




    path('customer/',views.customer,name='customer'),
    path('store/manager',views.store_manager,name='store_manager'),
    path('agent',views.agent,name='agent'),
]