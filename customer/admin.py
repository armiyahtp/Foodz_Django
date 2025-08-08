from django.contrib import admin

from customer.models import *


admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Offer)
admin.site.register(CartBill)


