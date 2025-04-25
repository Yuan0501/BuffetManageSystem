from django.contrib import admin
from .models import Department, UserInfo, Price;


# Register your models here.
admin.site.register(Department)
admin.site.register(UserInfo)
admin.site.register(Price)
