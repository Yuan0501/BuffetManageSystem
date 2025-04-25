from django.contrib import admin
from .models import Order_new, OrderItem

# Register your models here.
admin.site.register(Order_new)
admin.site.register(OrderItem)