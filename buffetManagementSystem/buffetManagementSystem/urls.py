"""
URL configuration for day16 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path

from app01.views import depart, user, price, index, admin, chart
from orderApp.views import OrderListView, OrderCreateView, add_price


# from orderApp import views as order

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('depart/list/', depart.depart_list, name='depart_list'),
    path('depart/add/', depart.depart_add),
    path('depart/delete/', depart.depart_delete),
    path('depart/edit/', depart.depart_edit),
    path('depart/detail/', depart.depart_detail),

    path('user/list/', user.user_list, name='user_list'),
    path('user/add/', user.user_add),
    path('user/delete/', user.user_delete),
    path('user/edit/', user.user_edit),
    path('user/detail/', user.user_detail),

    path('price/list/', price.price_list, name='item_list'),
    path('price/add/', price.price_add),
    path('price/<int:nid>/edit/', price.price_edit),
    path('price/delete/', price.price_delete),
    # path('get_price/<int:item_id>/', order.get_price, name='get_price'),

    path('admin/list/', admin.admin_list, name='admin_list'),
    path('admin/add/', admin.admin_add),
    path('admin/edit/<int:nid>/', admin.admin_edit),
    path('admin/delete/', admin.admin_delete),
    path('admin/reset/<int:nid>/', admin.admin_reset),

    path('login/', index.login),
    path('logout/', index.logout),
    path('index/', index.index, name='home'),
    path('about/', index.about),
    path('contact/', index.contact),



# Order related URLs
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('orders/new/', OrderCreateView.as_view(), name='order_create'),
    path('prices/add/',add_price, name='add_price'),

    path('chart/list/', chart.chart_list, name='chart_list'),

]
