from django import forms

from restaurant.models import *
from customer.models import *
from manager.models import Manager
from users.models import User


class StoreCategoryForm(forms.ModelForm):
    class Meta:
        model = StoreCategory
        fields = ["name", "image"]


        widgets = {
            "name":forms.widgets.TextInput(attrs={"class": "form-control" ,"placeholder": "Category name"}),
            "image":forms.widgets.FileInput(attrs={"class": "form-control"})
        }
        



class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ["name", "tagline", "category", "image", "rating", "time", "offer"]

        widgets = {
            "name":forms.widgets.TextInput(attrs={"class": "form-control", "placeholder": "Store name"}),
            "image":forms.widgets.FileInput(attrs={"class": "form-control"}),
            "tagline":forms.widgets.TextInput(attrs={"class": "form-control", "placeholder": "Tagline"}),
            "category":forms.widgets.Select(attrs={"class": "form-control",}),
            "rating":forms.widgets.NumberInput(attrs={"class": "form-control", "placeholder": "Rating"}),
            "time":forms.widgets.NumberInput(attrs={"class": "form-control", "placeholder": "Time"}),
            "offer":forms.widgets.TextInput(attrs={"class": "form-control", "placeholder": "Store ofer"}),
        }





class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = ["name", "image", "store"]


        widgets = {
            "name":forms.widgets.TextInput(attrs={"class":"form-control", "placeholder" : "Slider Name"}),
            "image":forms.widgets.FileInput(attrs={"class":"form-control"}),
            "store":forms.widgets.Select(attrs={"class":"form-control"}),
        }





class FoodCategoryForm(forms.ModelForm):
    class Meta:
        model = FoodCategory
        fields = ["name", "store"]


        widgets = {
            "name":forms.widgets.TextInput(attrs={"class":"form-control", "placeholder":"Category Name"}),
            "store":forms.widgets.Select(attrs={"class":"form-control"}),
        }







class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ["name", "image", "price", "categry", "is_veg"]


        widgets = {
            "name":forms.widgets.TextInput(attrs={"class":"form-control","placeholder":"Food Item Name"}),
            "image":forms.widgets.FileInput(attrs={"class":"form-control"}),
            "price":forms.widgets.NumberInput(attrs={"class":"form-control", "placeholder":"Price"}),
            "categry":forms.widgets.Select(attrs={"class":"form-control"}),
            "is_veg":forms.widgets.CheckboxInput(attrs={"class":"form-check-input"}),
        }







class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ["coupon_code", "description", "offer","is_percentage"]


        widgets = {
            "coupon_code":forms.widgets.TextInput(attrs={"class":"form-control","placeholder":"Coupen Code"}),
            "description":forms.widgets.TextInput(attrs={"class":"form-control","placeholder":"Offer Description"}),
            "offer":forms.widgets.NumberInput(attrs={"class":"form-control", "placeholder":"Offer Amount"}),
            "is_percentage":forms.widgets.CheckboxInput(attrs={"class":"form-check-input"}),
        }

