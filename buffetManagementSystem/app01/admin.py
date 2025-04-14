from django.contrib import admin
from .models import Department, UserInfo, Price, Order;


# Register your models here.
admin.site.register(Department)
admin.site.register(UserInfo)
admin.site.register(Price)
admin.site.register(Order)