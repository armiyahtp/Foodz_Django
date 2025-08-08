from django.shortcuts import render,reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count

from users.models import User
from customer.models import *

from restaurant.models import StoreCategory, Store, Slider,FoodCategory, FoodItem




@login_required(login_url='/login')
def index(request):
    store_categories = StoreCategory.objects.all()
    stores = Store.objects.all()
    sliders = Slider.objects.all()

    context = {
        "store_categories" : store_categories,
        "stores" : stores,
        "sliders" : sliders
    }
    return render(request, 'web/index.html', context=context)




def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(reverse('web:index'))

        else:
            context = {
                "error" : True,
                "message": "Invalid Email or Password"
            }
            return render(request, 'web/login.html', context=context)
    else:         
        return render(request, 'web/login.html')




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
            return render(request, 'web/register.html', context=context)

        else:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                is_customer=True
            )
            user.save()

            customer = Customer.objects.create(
                user=user
            )
            customer.save()
            return HttpResponseRedirect(reverse('web:login'))

    else:
        return render(request, 'web/register.html')
    



def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('web:login'))





@login_required(login_url='/login')
def restaurants(request, id):
    store_categories = StoreCategory.objects.all()
    stores = Store.objects.all()

    selected_category = StoreCategory.objects.get(id=id)
    store = stores.filter(category=selected_category)


    context = {
        "store_categories" : store_categories,
        "store" : store,
    }
    return render(request, 'web/restaurant.html', context=context)



@login_required(login_url='/login')
def single_restaurant(request,id):
    user = request.user
    customer = Customer.objects.get(user=user)
    store = Store.objects.get(id=id)
    food_categories = FoodCategory.objects.filter(store=store)
    products = FoodItem.objects.filter(categry__store=store)
    carts = Cart.objects.filter(customer=customer)


    product_with_quantities =[]
    for product in products:
        item_cart = carts.filter(product=product).first()

        if item_cart:
            quantity = item_cart.qty
        else:
            quantity = 0


        product_with_quantities.append({
            'product' : product,
            'quantity' : quantity,
            'cart' : item_cart,
        })


    items = 0
    amount = 0
    for cart in carts:
        items = items + 1
        amount = amount + cart.amnt
        

    

    context = {
        "store" : store,
        "food_categories"  : food_categories,
        "items" : items,
        "amount" : amount,
        "carts": carts,
        "product_with_quantities" : product_with_quantities,
    }
    return render(request, 'web/singlerest.html', context=context)



@login_required(login_url='/login')
def cart(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    carts = Cart.objects.filter(customer=customer)
    addresses = Address.objects.filter(customer=customer)
    


    if CartBill.objects.filter(customer=customer).exists():
        cart_bill = CartBill.objects.get(customer=customer)
    else:
        cart_bill = CartBill.objects.create(
            customer=customer,
        ) 
        cart_bill.save()



    selected_address= None
    for address in addresses:
        if address.is_selected:
            selected_address = address


    
    store = None
    for cart in carts:
        store = cart.store

    sub_total = carts.aggregate(Sum('amnt'))['amnt__sum'] or 0 
    total = sub_total - cart_bill.offer_amnt 
    


    context = {
        "store" : store,
        "carts" : carts,
        "selected_address" : selected_address,
        "sub_total" : sub_total,
        "total" : total,
        "cart_bill" : cart_bill,
    }
    return render(request, 'web/cart.html', context=context)




@login_required(login_url='/login')
def offers(request):
    offers = Offer.objects.all()

    context = {
        "offers" : offers
    }
   
    return render(request, 'web/offers.html', context=context)




@login_required(login_url='/login')
def checkout(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    carts = Cart.objects.filter(customer=customer)
    cart_bill = CartBill.objects.get(customer=customer)


    sub_total = carts.aggregate(Sum('amnt'))['amnt__sum'] or 0
    total = sub_total-cart_bill.offer_amnt

    context = {
        "sub_total" : sub_total,
        "carts" : carts,
        "total" : total,
        "cart_bill" : cart_bill,
    }   
    return render(request, 'web/checkout.html', context=context)



@login_required(login_url='/login')
def account(request):
    user=request.user
    customer=Customer.objects.get(user=user)
    orders=Order.objects.filter(customer=customer)
    
    order_item_count = []
    order_count = 0

    
    for order in orders:
        if order_count < 4:
            order_count += 1    
            count = OrderItem.objects.filter(order=order).count()
            order_item_count.append({
                "order" : order,
                "count" : count,
            })




    context = {
        "orders" : orders,
        "order_item_count" : order_item_count,
        "customer" : customer,
        "order_count" : order_count,
    }
    return render(request, 'web/account.html', context=context)




@login_required(login_url='/login')
def cart_add(request,id):
    user = request.user
    customer = Customer.objects.get(user=user)
    product = FoodItem.objects.get(id=id)
    store = product.categry.store
    price = product.price

    carts = Cart.objects.filter(customer=customer)

    for cart in carts:
        cart_store = cart.store

        if not store == cart_store:
            cart.delete()


    cart = Cart.objects.create(
        customer=customer,
        product=product,
        qty=1,
        store=store,
        amnt=price
    )

    cart.save()





    return HttpResponseRedirect(reverse('web:single_restaurant',kwargs={"id":store.id}))




@login_required(login_url='/login')
def cart_plus(request,id):
    cart = Cart.objects.get(id=id)
    price = cart.product.price

    cart.qty = cart.qty + 1
    cart.amnt = cart.amnt + price

    cart.save()

    return HttpResponseRedirect(reverse('web:cart'))




@login_required(login_url='/login')
def cart_minus(request,id):
    cart = Cart.objects.get(id=id)
    price = cart.product.price

    if cart.qty > 1:
        cart.qty = cart.qty - 1
        cart.amnt = cart.amnt - price

        cart.save()

    else:
        cart.delete()

    return HttpResponseRedirect(reverse('web:cart'))




@login_required(login_url='/login')
def rest_cart_plus(request,id):
    cart = Cart.objects.get(id=id)
    price = cart.product.price
    store = cart.store

    cart.qty = cart.qty + 1
    cart.amnt = cart.amnt + price

    cart.save()

    return HttpResponseRedirect(reverse('web:single_restaurant',kwargs={"id":store.id}))




@login_required(login_url='/login')
def rest_cart_minus(request,id):
    cart = Cart.objects.get(id=id)
    price = cart.product.price
    store = cart.store

    if cart.qty > 1:
        cart.qty = cart.qty - 1
        cart.amnt = cart.amnt - price

        cart.save()

    else:
        cart.delete()

    return HttpResponseRedirect(reverse('web:single_restaurant',kwargs={"id":store.id}))




@login_required(login_url='/login')
def address(request):
    user = request.user
    customer=Customer.objects.get(user=user)
    addresses = Address.objects.filter(customer=customer)


    
    context = {
        "addresses" : addresses,

    }
    return render(request, 'web/address.html', context=context)




@login_required(login_url='/login')
def add_address(request):
    user = request.user
    customer = Customer.objects.get(user=user)

    if request.method == 'POST':
        address = request.POST.get('address')
        appartment = request.POST.get('appartment')
        landmark = request.POST.get('landmark')
        address_type = request.POST.get('address_type')

        customer_address = Address.objects.create(
            customer=customer,
            address=address,
            appartment=appartment,
            landmark=landmark,
            address_type=address_type,
        )

        customer_address.save()

        return HttpResponseRedirect(reverse('web:address'))
    
    else:

        return render(request, 'web/add_address.html')




@login_required(login_url='/login')
def edit_address(request, id):
    addr = Address.objects.get(id=id)

    if request.method == 'POST':

        address = request.POST.get('address')
        appartment = request.POST.get('appartment')
        landmark = request.POST.get('landmark')
        address_type = request.POST.get('address_type')


        addr.address = address
        addr.appartment = appartment
        addr.landmark = landmark
        addr.address_type = address_type

        addr.save()

        return HttpResponseRedirect(reverse('web:address'))
    
    else:

        context = {
            "address" : addr,
        }

        return render(request, 'web/add_address.html', context=context)




@login_required(login_url='/login')
def delete_address(request, id):
    address = Address.objects.get(id=id)
    address.delete()

    return HttpResponseRedirect(reverse('web:address'))





def select_address(request, id):
    selected_address = Address.objects.get(id=id)
    addresses = Address.objects.all()


    for address in addresses:
        if address == selected_address:
            address.is_selected=True
            address.save()

        else:
            address.is_selected=False
            address.save()

          

    return HttpResponseRedirect(reverse('web:address'))


def place_order(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    addresses = Address.objects.filter(customer=customer)
    cart_bill = CartBill.objects.get(customer=customer)

    for addr in addresses:
        if addr.is_selected:
            address=addr

    carts = Cart.objects.filter(customer=customer)
    for cart in carts:
        store = cart.store

    sub_total = carts.aggregate(Sum('amnt'))['amnt__sum']
    total = sub_total-cart_bill.offer_amnt

    previus = Order.objects.filter(customer=customer).first()

    if previus:
        order_id=f'ORD000{previus.id+1}'
    else:
        order_id='ORD0001'

    order = Order.objects.create(
        order_id=order_id,
        customer=customer,
        address=address,
        sub_total=sub_total,
        status='PL',
        total=total,
        store=store,
    )

    for cart in carts:
        order_item=OrderItem.objects.create(
           customer = customer,
           order = order,
           product=cart.product,
           qty= cart.qty,
           store=cart.store,
           amnt=cart.amnt
        )
        cart.delete()

        cart_bill.offer_amnt = 0
        cart_bill.coupen_code = None
        cart_bill.save()

    return HttpResponseRedirect(reverse('web:account'))


def offer_apply(request,id):
    user = request.user
    customer = Customer.objects.get(user=user)
    offer = Offer.objects.get(id=id)
    total = Cart.objects.filter(customer=customer).aggregate(Sum('amnt'))['amnt__sum']

    if offer.is_percentage:
        offer_amnt=total*(offer.offer/100)
    else:
        offer_amnt=offer.offer
    

    cart_bill = CartBill.objects.get(customer=customer)
    cart_bill.offer_amnt=offer_amnt
    cart_bill.coupen_code=offer.coupon_code
    cart_bill.save()


    return HttpResponseRedirect(reverse('web:cart'))





def orders(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    orders = Order.objects.filter(customer=customer)
    
    order_item_count = []

    for order in orders:   
        count = OrderItem.objects.filter(order=order).count()
        order_item_count.append({
            "order" : order,
            "count" : count,
        })

    context = {
        "orders" : orders,
        "order_item_count" : order_item_count,
        "customer" : customer,
    }
    return render(request, 'web/orders.html', context=context)



def order_tracking(request, id):
    user = request.user
    customer = Customer.objects.get(user=user)
    order = Order.objects.get(id=id, customer=customer)
    order_items = OrderItem.objects.filter(order=order)
    is_numeric = order.address.appartment.isdigit()
    offer = order.sub_total - order.total 


    steps = [
        {"label": "Order Placed", "completed": False},
        {"label": "Processed", "completed": False},
        {"label": "Shipped", "completed": False},
        {"label": "Out for Delivery", "completed": False},
        {"label": "Delivered", "completed": False},
    ]

    if order.status == 'PL':
        status = 0
        for i in range(status + 1):
            steps[i]['completed'] = True
    elif order.status == 'AC':
        status = 1
        for i in range(status + 1):
            steps[i]['completed'] = True
    elif order.status == 'SH':
        status = 2
        for i in range(status + 1):
            steps[i]['completed'] = True
    elif order.status == 'DI':
        status = 3
        for i in range(status + 1):
            steps[i]['completed'] = True
    elif order.status == 'CO':
        status = 4
        for i in range(status + 1):
            steps[i]['completed'] = True
    else:
        status = 0


    context = {
        "order": order,
        "steps": steps,
        "is_numeric" : is_numeric,
        "order_items": order_items,
        "offer": offer,
    }

    return render(request, 'web/order-track.html', context=context)
