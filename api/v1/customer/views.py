from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


from django.contrib.auth import authenticate
from users.models import User
from customer.models import Customer
from api.v1.customer.serializers import *



@api_view(['POST'])
@permission_classes ([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(email=email, password=password)

    if user:
        refresh = RefreshToken.for_user(user)
        response_data = {  
            "status_code": 6000,
            "data": {
                "access": str(refresh.access_token),
            },
            "message": "User is authenticated successfully"
        }
    else:
        response_data = {
            "status_code": 6001,
            "message": "Invalid credentials"
        }

    return Response(response_data)




@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    email = request.data.get('email')
    password = request.data.get('password')

    if User.objects.filter(email=email).exists():
        response_data = {
            "status_code": 6002,
            "message": "Email already exists"
        }
        return Response(response_data)

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

    rfersh = RefreshToken.for_user(user)
    response_data = {
        "status_code": 6000,
        "data": {
            "access": str(rfersh.access_token),
        },
        "message": "User is registered successfully"
    }

    return Response(response_data)
















@api_view(['GET'])
@permission_classes([IsAuthenticated])
def account(request):
    user = request.user
    customer = Customer.objects.get(user=user)

    response_data = {
        "status_code": 6000,
        "data": {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "customer_id": customer.id
        },
        "message": "User account information"
    }
    return Response(response_data)











@api_view(["GET"])
@permission_classes([IsAuthenticated])
def address(request):
    user = request.user
    customer = Customer.objects.get(user=user)


    instances = Address.objects.filter(customer=customer)
    context = {
        "request":request
    }


    serializer = AddressSerializer(instances, many=True, context=context)


    response_data = {
        "status_code":6000,
        "data":serializer.data,
        "message": "Address List"
    }


    return Response(response_data)




@api_view(["POST"])
@permission_classes([IsAuthenticated])
def address_add(request):
    user = request.user
    customer = Customer.objects.get(user=user)


    address = request.data.get('address')
    appartment = request.data.get('appartment')
    landmark = request.data.get('landmark')
    address_type = request.data.get('address_type')

    customer_address = Address.objects.create(
        customer=customer,
        address=address,
        appartment=appartment,
        landmark=landmark,
        address_type=address_type,
    )

    customer_address.save()

    response_data = {
        "status_code":6000,
        "data":{},
        "maessage":"Address Added" 
    }

    return Response(response_data)





@api_view(["PUT"])  
@permission_classes([IsAuthenticated])
def address_update(request,id):
    instance = Address.objects.get(id=id)
    

    address = request.data.get('address')
    appartment = request.data.get('appartment')
    landmark = request.data.get('landmark')
    address_type = request.data.get('address_type')


    instance.address =address
    instance.appartment=appartment
    instance.landmark=landmark
    instance.address_type=address_type

    instance.save()


    response_data = {
        "status_code":6000,
        "data":{},
        "message":"Address Updated"
    }

    return Response(response_data)





@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def address_delete(request,id):
    instance = Address.objects.get(id=id)
    instance.delete()

    response_data = {
        "status_code":6000,
        "data":{},
        "message":"Address Deleted"
    }

    return Response(response_data)












@api_view(['GET'])
@permission_classes([AllowAny])
def slider(request):
    instances = Slider.objects.all()

    context = {
        "request": request,
    }
    serializer = SliderSerializer(instances, many=True, context=context)

    response_data = {
        'status_code': 6000,
        'data': serializer.data,
        'message': 'slider list retrieved successfully'
    }
    return Response(response_data)




@api_view(['GET'])
@permission_classes([AllowAny])
def store(request):

    instances = Store.objects.all()

    context = {
        "request":request,
        
    }
    serializer = StoreSerializer(instances, many=True, context=context)

    response_data = {
        'status_code': 6000,
        'data': serializer.data,
        'message': 'Store list retrieved successfully'
    }
    return Response(response_data)




@api_view(['GET'])
@permission_classes([AllowAny])
def store_category(request):
    instances = StoreCategory.objects.all()

    context = {
        "request":request
    }
    serializer = StoreCategorySerializer(instances, many=True, context=context)

    response_data = {
        'status_code': 6000,
        'data': serializer.data,
        'message': 'store category list retrieved successfully'
    }
    return Response(response_data)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def food_category(request):
    instances = FoodCategory.objects.all()

    context = {
        "request": request
    }
    serializer = FoodCategorySerializer(instances, many=True, context=context)

    response_data = {
        'status_code': 6000,
        'data': serializer.data,
        'message': 'Food category list retrieved successfully'
    }
    return Response(response_data)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def food_items(request):
    instances = FoodItem.objects.all()
    context = {
        "request": request
    }
    serializer = FoodItemSerializer(instances, many=True, context=context)
    response_data = {
        'status_code': 6000,
        'data': serializer.data,
        'message': 'Food items list retrieved successfully'
    }
    return Response(response_data)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def single_rest(request, id):

    instance = Store.objects.get(id=id)

    context = {
        "request":request
    }
    seriralizer = StoreSerializer(instance, context=context)
    response_data = {
        'status_code': 6000,
        'data': seriralizer.data,
        'message' : 'single restaurant data retrieved successfully'
    }
    return Response(response_data)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cart(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    instances = Cart.objects.filter(customer=customer)
    context = {
        "request":request
    }
    serializer = CartSerializer(instances, many=True, context=context)
    response_data = {
        'status_code': 6000,
        'data': serializer.data,
        'message': 'Cart items retrieved successfully'
    }
    return Response(response_data)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def offer(request):

    instances = Offer.objects.all()
    context = {
        "request": request
    }
    serializer = OfferSerializer(instances, many=True, context=context)
    response_data = {
        'status_code': 6000,
        'data': serializer.data,
        'message': 'offer list retrieved successfully'

    }
    return Response(response_data)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order(request):
    user = request.user
    customer =Customer.objects.get(user=user)
    instances = Order.objects.filter(customer=customer)
    context = {
        "request": request
    }
    serializer = OrderSerializer(instances, many=True,context=context)
    response_data = {
        'status_code': 6000,
        'data':serializer.data,
        'message': 'Order list retrieved successfully'
    }
    return Response(response_data)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_item(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    instances = OrderItem.objects.filter(customer=customer)
    context = {
        "request": request
    }
    serializer = OrderItemSerializer(instances, many=True,context=context)

    response_data = {
        'status_code':6000,
        'data':serializer.data,
        'message':'Order item list retrieved successfully'
    }
    return Response(response_data)

