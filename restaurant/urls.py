from django.urls import path
from restaurant import views

app_name = "restaurant"


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add_store/', views.add_store, name='add_store'),
    path('edit_store/<int:id>/', views.edit_store, name='edit_store'),
    path('delete_store/<int:id>/', views.delete_store, name='delete_store'),
 


    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),




    path('food-items/', views.food_items, name='food_items'),
    path('single_food_item/<int:id>/', views.single_food_item, name='single_food_item'),
    path('add_food_item/', views.add_food_item, name='add_food_item'),
    path('edit_food_item/<int:id>/', views.edit_food_item, name='edit_food_item'),
    path('delete_food_item/<int:id>/', views.delete_food_item, name='delete_food_item'),





    path('food-categories/', views.food_categories, name='food_categories'),
    path('add_food_category/', views.add_food_category, name='add_food_category'),
    path('edit_food_category/<int:id>/', views.edit_food_category, name='edit_food_category'),
    path('delete_food_category/<int:id>/', views.delete_food_category, name='delete_food_category'),







    path('orders/', views.orders, name='orders'),
    path('order/<int:id>/',views.order,name='order'),
    path('order/delete/<int:id>/',views.order_delete,name='order_delete'),
]