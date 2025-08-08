from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as login_manager, logout as logout_manager
from restaurant.models import *
from manager.forms import *
from customer.models import *
from users.models import User
from main.decorators import allow_super
from main.function import generate_form_errors





 



@login_required(login_url='/manager/login')
@allow_super
def dashboard(request):
    instances = Order.objects.all()
    orders = instances.count()
    stores = Store.objects.all().count()
    customers = Customer.objects.all().count()
    earnings = 0
    for order in instances:
        earnings += ((5 * order.total) / 100)

    context = {
        "instances" : instances,
        "orders" : orders,
        "stores" : stores,
        "customers" : customers,
        "earnings" : earnings
    }
    return render(request, 'manager/index.html', context=context)


@login_required(login_url='/manager/login')
@allow_super
def profile(request):
    user = request.user
    manager = get_object_or_404(Manager, user=user)
    context = {
        "manager": manager
    }
    return render(request, 'manager/profile.html', context=context)








def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(email=email).exists():
            message = "Email already exists"
            context = {
                "message": message,
            }
            return render(request, 'manager/register.html', context=context)
        else:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                is_superuser=True,
                is_staff=True,
                is_manager=True
            )
            user.save()
            manager = Manager.objects.create(user=user)
            manager.save()

            return HttpResponseRedirect(reverse('manager:login'))
        
    else:
        return render(request, 'manager/register.html')
    

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_superuser:
            login_manager(request, user)
            return HttpResponseRedirect(reverse('manager:dashboard'))
        else:
            message = "Invalid email or password"
            context = {
                "message": message,
            }
            return render(request, 'manager/login.html', context=context)

    else:
        return render(request, 'manager/login.html')


@allow_super
def logout(request):
    logout_manager(request)
    return HttpResponseRedirect(reverse('manager:login'))














@login_required(login_url='/manager/login')
@allow_super
def store_category(request):
    instances = StoreCategory.objects.all()


    context = {
        "instances" : instances
    }
    return render(request, "manager/store-categories.html", context=context)


@login_required(login_url='/manager/login')
@allow_super
def store_category_create(request):
    if request.method == 'POST':
        form = StoreCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            return HttpResponseRedirect(reverse('manager:store_category'))

        else:
            message = generate_form_errors(form)
            form = StoreCategoryForm()
            context = {
                "form": form,
                "errors": True,
                "message": message,
            }
            return render(request, "manager/add-store-categories.html", context=context)

    else:
        form = StoreCategoryForm()
        context = {
            "form": form,
        }
        return render(request, "manager/add-store-categories.html", context=context)
    

@login_required(login_url='/manager/login')
@allow_super
def store_category_update(request, id):
    instance = get_object_or_404(StoreCategory, id=id)

    if request.method == 'POST':
        form = StoreCategoryForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            return HttpResponseRedirect(reverse('manager:store_category'))

        else:
            message = generate_form_errors(form)
            form = StoreCategoryForm(instance=instance)
            context = {
                "form": form,
                "errors": True,
                "message": message,
            }
            return render(request, "manager/add-store-categories.html", context=context)
            
            

    else:
        form = StoreCategoryForm(instance=instance)
        context = {
            "form": form,
        }
        return render(request, "manager/add-store-categories.html", context=context)


@login_required(login_url='/manager/login')
@allow_super
def store_category_delete(request, id):
    instance = get_object_or_404(StoreCategory, id=id)
    instance.delete()

    return HttpResponseRedirect(reverse('manager:store_category'))











@login_required(login_url='/manager/login')
@allow_super
def order(request, id):
        instance = get_object_or_404(Order, id=id)

        context = {
            "instance": instance,
        }
        return render(request, "manager/order.html", context=context)


@login_required(login_url='/manager/login')
@allow_super 
def order_assign(request, id):
    pass


@login_required(login_url='/manager/login')
@allow_super
def order_accept(request, id):
    order = Order.objects.get(id=id)

    order.status = 'AC'
    order.save()

    return HttpResponseRedirect(reverse('manager:dashboard'))


@login_required(login_url='/manager/login')
@allow_super
def order_reject(request, id):
    order = Order.objects.get(id=id)

    order.status = 'CA'
    order.save()
    return HttpResponseRedirect(reverse('manager:dashboard'))


@login_required(login_url='/manager/login')
@allow_super
def order_prepared(request, id):
    order = Order.objects.get(id=id)

    order.status = 'SH'
    order.save()

    return HttpResponseRedirect(reverse('manager:dashboard'))


@login_required(login_url='/manager/login')
@allow_super
def order_picked(request, id):
    order = Order.objects.get(id=id)

    order.status = 'DI'
    order.save()

    return HttpResponseRedirect(reverse('manager:dashboard'))


@login_required(login_url='/manager/login')
@allow_super
def order_completed(request, id):

    instance  = get_object_or_404(Order, id=id)
    instance.status = 'CO'
    instance.save()
    return HttpResponseRedirect(reverse('manager:dashboard'))



@login_required(login_url='/manager/login')
@allow_super
def order_delete(request, id):

    instance  = get_object_or_404(Order, id=id)
    instance.delete()
    return HttpResponseRedirect(reverse('manager:dashboard'))












@login_required(login_url='/manager/login')
@allow_super
def store(request):
    instances = Store.objects.all()

    context = {
        "instances" : instances
    }
    return render(request, 'manager/stores.html', context=context)


@login_required(login_url='/manager/login')
@allow_super
def single_store(request, id):
    instance = get_object_or_404(Store, id=id)

    context = {
        "instance" : instance
    }
    return render(request, 'manager/store.html', context=context)
    

@login_required(login_url='/manager/login')
@allow_super
def store_create(request):
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            return HttpResponseRedirect(reverse('manager:store'))

        else:
            message = generate_form_errors(form)
            form = StoreForm()
            context = {
                "form": form,
                "errors": True,
                "message": message,
            }
            return render(request, "manager/add-store.html", context=context)
            

    
    else:
        form = StoreForm()
    context = {
        "form":form
    }
    return render(request, 'manager/add-store.html', context=context)


@login_required(login_url='/manager/login')
@allow_super
def store_update(request,id):
    instance = get_object_or_404(Store, id=id)

    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            return HttpResponseRedirect(reverse('manager:store'))

        else:
            message = generate_form_errors(form)
            form = StoreForm(instance=instance)
            context = {
                "form": form,
                "errors": True,
                "message": message,
            }
            return render(request, "manager/add-store.html", context=context)
            

    
    else:
        form = StoreForm(instance=instance)
    context = {
        "form":form
    }
    return render(request, 'manager/add-store.html', context=context)


@login_required(login_url='/manager/login')
@allow_super
def store_delete(request,id):

    instance = get_object_or_404(Store, id=id)
    instance.delete()
    return HttpResponseRedirect(reverse('manager:store'))












@login_required(login_url='/manager/login')
@allow_super
def food_category(request):
    instances = FoodCategory.objects.all()

    context = {
        "instances":instances
    }
    return render(request, 'manager/food-categories.html', context=context)


@login_required(login_url='/manager/login')
@allow_super
def food_category_create(request):
    if request.method == 'POST':
        form = FoodCategoryForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            return HttpResponseRedirect(reverse('manager:food_category'))
        
        else:
            message = generate_form_errors(form)
            form = FoodCategoryForm()
            context = {
                "form": form,
                "errors": True,
                "message": message,
            }
            return render(request, 'manager/add-food-categories.html', context=context)
            

    else:
        form = FoodCategoryForm()

        context = {
            "form":form
        }
        return render(request, 'manager/add-food-categories.html', context=context)


@login_required(login_url='/manager/login')
@allow_super
def food_category_update(request,id):
    instance = get_object_or_404(FoodCategory, id=id)
    if request.method == 'POST':
        form = FoodCategoryForm(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            return HttpResponseRedirect(reverse('manager:food_category'))
        
        else:
            message = generate_form_errors(form)
            form = FoodCategoryForm(instance=instance)
            context = {
                "form": form,
                "errors": True,
                "message": message,
            }
            return render(request, 'manager/add-food-categories.html', context=context)
            

    else:
        form = FoodCategoryForm(instance=instance)

        context = {
            "form":form
        }
        return render(request, 'manager/add-food-categories.html', context=context)


@login_required(login_url='/manager/login')
@allow_super
def food_category_delete(request,id):
    instance = get_object_or_404(FoodCategory, id=id)
    instance.delete()

    return HttpResponseRedirect(reverse('manager:food_category'))












@login_required(login_url='/manager/login')
@allow_super
def food_item(request):
    instances = FoodItem.objects.all()

    context = {
        "instances":instances
    }
    return render(request, 'manager/food-items.html', context=context)


@login_required(login_url='/manager/login')
@allow_super
def single_food_item(request,id):
    instance = get_object_or_404(FoodItem, id=id)

    context = {
        "instance":instance
    }
    return render(request, 'manager/food-item.html', context=context)


@login_required(login_url='/manager/login')
@allow_super
def food_item_create(request):
    if request.method == "POST":
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            return HttpResponseRedirect(reverse('manager:food_item'))
        
        else:
            message = generate_form_errors(form)
            form = FoodItemForm()
            context = {
                "form": form,
                "errors": True,
                "message": message,
            }
            return render(request, 'manager/add-food-items.html', context=context)
            

    else:
        form = FoodItemForm()
        context = {
            "form":form,
        }
        return render(request, 'manager/add-food-items.html', context=context)


@login_required(login_url='/manager/login')
@allow_super
def food_item_update(request,id):
    instance = get_object_or_404(FoodItem, id=id)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            return HttpResponseRedirect(reverse('manager:food_item'))
        
        else:
            message = generate_form_errors(form)
            form = FoodItemForm(instance=instance)
            context = {
                "form": form,
                "errors": True,
                "message": message,
            }
            return render(request, 'manager/add-food-items.html', context=context)

            

    else:
        form = FoodItemForm(instance=instance)

        context = {
            "form":form
        }
        return render(request, 'manager/add-food-items.html', context=context)


@login_required(login_url='/manager/login')
@allow_super
def food_item_delete(request,id):
    instance = get_object_or_404(FoodItem,id=id)
    instance.delete()

    return HttpResponseRedirect(reverse('manager:food_item'))












@login_required(login_url='/manager/login')
@allow_super
def slider(request):
    instances = Slider.objects.all()

    context = {
        "instances":instances
    }
    return render(request, 'manager/sliders.html', context=context)


@login_required(login_url='/manager/login')
@allow_super
def slider_create(request):
    if request.method == 'POST':
        form = SliderForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            return HttpResponseRedirect(reverse('manager:slider'))
        else:
            message = generate_form_errors(form)
            form = SliderForm()
            context = {
                "form": form,
                "errors": True,
                "message": message,
            }
            return render(request, 'manager/add-slider.html', context=context)
            
    else:
        form = SliderForm()

        context = {
            "form":form
        }

        return render(request, 'manager/add-slider.html', context=context)


@login_required(login_url='/manager/login')
@allow_super
def slider_update(request,id):
    instance = get_object_or_404(Slider, id=id)
    if request.method == 'POST':
        form = SliderForm(request.POST, request.FLES, instance=instance)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.save()

            return HttpResponseRedirect(reverse('manager:slider'))

        else:
            message = generate_form_errors(form)
            form = SliderForm(instance=instance)
            context = {
                "form": form,
                "errors": True,
                "message": message,
            }
            return render(request, 'manager/add-slider.html', context=context)
            

    
    else:
        form = SliderForm(instance=instance)

        context = {
            "form" : form
        }
        return render(request, 'manager/add-slider.html', context=context)
    

@login_required(login_url='/manager/login')
@allow_super
def slider_delete(request,id):
    instance = get_object_or_404(Slider, id=id)
    instance.delete()

    return HttpResponseRedirect(reverse('manager:slider'))

















@login_required(login_url='/manager/login')
@allow_super
def carts(request):
    instances = Cart.objects.all()

    context = {
        "instances" : instances
    }  
    return render(request, 'manager/carts.html',context=context)



@login_required(login_url='/manager/login')
@allow_super
def carts_delete(request,id):
    instance = get_object_or_404(Cart, id=id)

    instance.delete() 
    return redirect('manager:carts')























@login_required(login_url='/manager/login')
@allow_super
def order_item(request):
    instances = OrderItem.objects.all()

    context = {
        "instances" : instances
    }  
    return render(request, 'manager/order-items.html',context=context)



@login_required(login_url='/manager/login')
@allow_super
def order_item_delete(request,id):
    instance = get_object_or_404(OrderItem, id=id)

    instance.delete() 
    return redirect('manager:order_item')




















@login_required(login_url='/manager/login')
@allow_super
def address(request):
    instances = Address.objects.all()

    context = {
        "instances" : instances
    }  
    return render(request, 'manager/address.html',context=context)



@login_required(login_url='/manager/login')
@allow_super
def address_delete(request,id):
    instance = get_object_or_404(Address, id=id)
    instance.delete()
    return render(request, 'manager/address.html')
















@login_required(login_url='/manager/login')
@allow_super
def offer(request):
    instances = Offer.objects.all()

    context = {
        "instances" : instances
    }  
    return render(request, 'manager/offers.html',context=context)



@login_required(login_url='/manager/login')
@allow_super
def offer_create(request):
    if request.method == 'POST':
        form = OfferForm(request.POST, request.FILES)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            return HttpResponseRedirect(reverse('manager:offer'))
        
        else:
            message = generate_form_errors(form)
            form = OfferForm()
            context = {
                "form": form,
                "errors": True,
                "message": message,
            } 
            return render(request, 'manager/add-offer.html',context=context)
        
    else:
        form = OfferForm()

        context = {
            "form":form
        }
        return render(request, 'manager/add-offer.html',context=context)



@login_required(login_url='/manager/login')
@allow_super
def offer_update(request, id):
    instance = get_object_or_404(Offer, id=id)
    if request.method == 'POST':
        form = OfferForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            return HttpResponseRedirect(reverse('manager:offer'))
        
        else:
            message = generate_form_errors(form)
            form = OfferForm()
            context = {
                "form": form,
                "errors": True,
                "message": message,
            } 
            return render(request, 'manager/add-offer.html',context=context)
        
    else:
        form = OfferForm(instance=instance)

        context = {
            "form":form
        }
        return render(request, 'manager/add-offer.html',context=context)



@login_required(login_url='/manager/login')
@allow_super
def offer_delete(request, id):
    instance = get_object_or_404(Offer, id=id)

    instance.delete() 
    return redirect('manager:offer')

















@login_required(login_url='/manager/login')
@allow_super
def customer(request):
    customers = Customer.objects.all()



    instances_list = []

    for customer in customers:
        orders = Order.objects.filter(customer=customer).count()
        instances_list.append({
            "customer":customer,
            "orders":orders
        })


    context = {
        "instances" : instances_list
    }  
    return render(request, 'manager/customers.html',context=context)



@login_required(login_url='/manager/login')
@allow_super
def store_manager(request):
    store_managers = StoreManager.objects.all()

    instance_list = []
    for store_manager in store_managers:
        orders = Order.objects.filter(store=store_manager.store).count()
        instance_list.append({
            "store_manager":store_manager,
            "orders":orders
        })

    context = {
        "instances" : instance_list
    }  
    return render(request, 'manager/store-manager.html',context=context)



@login_required(login_url='/manager/login')
@allow_super
def agent(request):

    context = {
        
    }  
    return render(request, 'manager/agents.html',context=context)