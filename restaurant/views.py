from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as login_store, logout as logout_store
from django.contrib.auth.decorators import login_required
from users.models import User
from restaurant.models import *
from customer.models import *
from manager.forms import StoreForm
from main.function import generate_form_errors
from main.decorators import allow_store



from restaurant.models import *
from main.function import generate_form_errors
from main.decorators import allow_store



@login_required(login_url='/restaurant/login')
@allow_store
def dashboard(request):
    user = request.user
    instance = StoreManager.objects.get(user=user).store
    
     
    
    orders = Order.objects.filter(store=instance)
    customers = orders.values('customer').distinct().count()
    fooditems = FoodItem.objects.filter(categry__store=instance).count()
    order_count = orders.count()
    

    earnings = 0
    for order in orders:
        earnings += (order.total - ((5 * order.total) / 100))

    context = {
        'instance': instance,
        'orders': order_count,
        'fooditems': fooditems,
        'earnings': earnings,
        'customers': customers,
    }
    return render(request, 'store/index.html', context=context)




@login_required(login_url='/restaurant/login')
@allow_store
def edit_store(request, id):
    instance = get_object_or_404(Store, id=id)

    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            return HttpResponseRedirect(reverse('restaurant:dashboard'))
        
        else:
            message = generate_form_errors(form)
            form = StoreForm(instance=instance)

            context = {
                "message":message,
                "error":True,
                "form":form,
            }
            return render(request, 'store/add-store.html', context=context)
        

    else:
        form = StoreForm(instance=instance)
        context = {
            'form':form
        }

        return render(request, 'store/add-store.html', context=context)


    

@login_required(login_url='/restaurant/login')
@allow_store
def add_store(request):
    user = request.user
    store_det = StoreManager.objects.get(user=user)

    if store_det.store:
        return HttpResponseRedirect(reverse('restaurant:profile'))
    
    else:
        if request.method == 'POST':
            form = StoreForm(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                store_det.store = instance
                store_det.save()
                return HttpResponseRedirect(reverse('restaurant:profile'))
            
            else:
                message = generate_form_errors(form)
                form = StoreForm()

                context = {
                    'message':message,
                    'error':True,
                    'form':form,
                }
                return render(request, 'store/add-store.html', context=context)

        else:
            form = StoreForm()
            context = {
                'form':form
            }
            return render(request, 'store/add-store.html', context=context)
    


@login_required(login_url='/restaurant/login')
@allow_store
def delete_store(request,id):
    instance = get_object_or_404(Store, id=id)
    instance.delete()

    return HttpResponseRedirect(reverse('restaurant:dashboard'))



@login_required(login_url='/restaurant/login')
@allow_store
def profile(request):
    user = request.user
    store_details = StoreManager.objects.get(user=user)
    store= store_details.store
    fooditems = FoodItem.objects.filter(categry__store=store).count()
    if store:
        orders = store_details.store.order_set.all().count()
    else:
        orders = 0

    context = {
        'store_details': store_details,
        'fooditems': fooditems,
        'orders': orders,
    }
    return render(request, 'store/profile.html', context=context)


















def register(request):
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')


        if User.objects.filter(email=email).exists():
            context = {
                "error" : True,
                "message": "Email already exists"
            }
            return render(request, 'store/register.html', context=context)
        

        else:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                is_store=True,
            )
            user.save()
            store_manager = StoreManager.objects.create(
                user=user,
            )
            store_manager.save()
            return HttpResponseRedirect(reverse('restaurant:login'))

    else:
        return render(request, 'store/register.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password, is_store=True)
        if user is not None:
            login_store(request, user)
            return HttpResponseRedirect(reverse('restaurant:dashboard'))
        else:
            message = "Invalid email or password"
            context = {
                "message": message,
            }
            return render(request, 'store/login.html', context=context)

    else:
        return render(request, 'store/login.html')


def logout(request):
    logout_store(request)
    return HttpResponseRedirect(reverse('restaurant:login'))















@login_required(login_url='/restaurant/login')
@allow_store
def food_items(request):
    user = request.user
    store_details = StoreManager.objects.get(user=user)
    store = store_details.store
    instances = FoodItem.objects.filter(categry__store=store)

    context = {
        'instances': instances,
    }
    return render(request, 'store/food-items.html', context=context)


@login_required(login_url='/restaurant/login')
@allow_store
def single_food_item(request,id):
    instance = get_object_or_404(FoodItem, id=id)
    context = {
        'instance': instance,
    }
    return render(request, 'store/food-item.html', context=context)


@login_required(login_url='/restaurant/login')
@allow_store
def add_food_item(request):
    user = request.user
    store = StoreManager.objects.get(user=user).store
    food_categories = FoodCategory.objects.filter(store=store)

    if request.method == 'POST':
        name = request.POST.get('fooditem_name')
        price = request.POST.get('price')
        is_veg = request.POST.get('is_veg') == 'on'
        category_id = request.POST.get('category')
        image = request.FILES.get('image')
        categry = get_object_or_404(FoodCategory, id=category_id)

        food_item = FoodItem.objects.create(
            name=name,
            price=price,
            is_veg=is_veg,
            categry=categry,
            image=image,
        )
        food_item.save()
        return HttpResponseRedirect(reverse('restaurant:food_items'))
    
    else:
        context = {
            "food_categories": food_categories
        }
        return render(request,'store/add-food-items.html', context=context)

    

@login_required(login_url='/restaurant/login')
@allow_store
def edit_food_item(request, id):
    instance = get_object_or_404(FoodItem, id=id)
    if request.method == 'POST':
        name = request.POST.get('fooditem_name')
        price = request.POST.get('price')
        is_veg = request.POST.get('is_veg') == 'on'
        category_id = request.POST.get('category')
        image = request.FILES.get('image')
        categry = get_object_or_404(FoodCategory, id=category_id)

        instance.name = name
        instance.price = price
        instance.is_veg = is_veg
        instance.categry = categry
        instance.image = image
        instance.save()
        return HttpResponseRedirect(reverse('restaurant:single_food_item', args=[id]))
    
    else:
        food_categories = FoodCategory.objects.filter(store=instance.categry.store)
        context = {
            'instance': instance,
            'food_categories': food_categories
        }
        return render(request,'store/add-food-items.html', context=context)



@login_required(login_url='/restaurant/login')
@allow_store
def delete_food_item(request, id):
    instance = get_object_or_404(FoodItem, id=id)
    instance.delete()
    return HttpResponseRedirect(reverse('restaurant:food_items'))















@login_required(login_url='/restaurant/login')
@allow_store
def food_categories(request):
    user = request.user
    store = StoreManager.objects.get(user=user).store

    instances = FoodCategory.objects.filter(store=store)
    context = {
        'instances': instances,
    }
    return render(request,'store/food-categories.html', context=context)



@login_required(login_url='/restaurant/login')
@allow_store
def add_food_category(request):
    user = request.user
    store = StoreManager.objects.get(user=user).store

    if request.method == 'POST':
        name = request.POST.get('category_name')
        food_category = FoodCategory.objects.create(
            name=name,
            store=store,
        )
        food_category.save()
        return HttpResponseRedirect(reverse('restaurant:food_categories'))
    
    else:
        return render(request,'store/add-food-categories.html')
    


@login_required(login_url='/restaurant/login')
@allow_store
def edit_food_category(request, id):
    instance = get_object_or_404(FoodCategory, id=id)
    if request.method == 'POST':
        name = request.POST.get('category_name')
        instance.name = name
        instance.save()
        return HttpResponseRedirect(reverse('restaurant:food_categories'))
    
    else:
        context = {
            'instance': instance
        }
        return render(request,'store/add-food-categories.html', context=context)
    


@login_required(login_url='/restaurant/login')
@allow_store
def delete_food_category(request, id):
    instance = get_object_or_404(FoodCategory, id=id)
    instance.delete()
    return HttpResponseRedirect(reverse('restaurant:food_categories'))















@login_required(login_url='/restaurant/login')
@allow_store
def orders(request):
    user = request.user
    store_details = StoreManager.objects.get(user=user)
    store = store_details.store
    instances = Order.objects.filter(store=store)
    context = {
        'instances': instances,
    }
    return render(request,'store/orders.html', context=context)



@login_required(login_url='/restaurant/login')
@allow_store
def order(request, id):
        instance = get_object_or_404(Order, id=id)

        context = {
            "instance": instance,
        }
        return render(request, "store/order.html", context=context)



@login_required(login_url='/restaurant/login')
@allow_store
def order_delete(request, id):

    instance  = get_object_or_404(Order, id=id)
    instance.delete()
    return HttpResponseRedirect(reverse('restaurant:dashboard'))