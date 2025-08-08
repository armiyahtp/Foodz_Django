from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from customer.models import *
from restaurant.models import *


class AddressSerializer(ModelSerializer):
    class Meta:
        fields = ("id","address","address_type","landmark","latitude","longitude","appartment","is_selected")
        model = Address






class SliderSerializer(ModelSerializer):
    class Meta:
        fields = ("id","name","image","store")
        model = Slider





class StoreCategorySerializer(ModelSerializer):
    class Meta:
        fields = ("id","name","image")
        model = StoreCategory




class StoreSerializer(ModelSerializer):
    class Meta:
        fields = ("id","name","tagline","category","image","rating","time","offer")
        model = Store





class FoodCategorySerializer(ModelSerializer):
    class Meta:
        fields = ("id","name","store")
        model = FoodCategory









class FoodItemSerializer(ModelSerializer):
    class Meta:
        fields = ("id","name","price","categry","image","is_veg")
        model = FoodItem








class CartSerializer(ModelSerializer):
    class Meta:
        fields = ("id","customer","product","qty","store","amnt")
        model = Cart








class OrderSerializer(ModelSerializer):
    class Meta:
        fields = ("id","customer","order_id","address","status","sub_total","total","store","delivery_charge")
        model = Order









class OrderItemSerializer(ModelSerializer):
    class Meta:
        fields = ("id","customer","order","product","qty","store","amnt")
        model = OrderItem







class OfferSerializer(ModelSerializer):
    class Meta:
        fields = ("id","coupon_code","description","offer","is_percentage")
        model = Offer