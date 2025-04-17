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
from django.contrib import admin
from django.urls import path

from app01.views import depart, user, order, price, admin, index

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('depart/list/', depart.depart_list),
    path('depart/add/', depart.depart_add),
    path('depart/delete/', depart.depart_delete),
    path('depart/edit/', depart.depart_edit),
    path('depart/detail/', depart.depart_detail),

    path('user/list/', user.user_list),
    path('user/add/', user.user_add),
    path('user/model/form/add/', user.user_model_form_add),

    path('order/list/', order.order_list),
    path('order/add/', order.order_add),
    path('order/<int:nid>/edit/', order.order_edit),
    path('order/<int:nid>/delete/', order.order_delete),

    path('price/list/', price.price_list),
    path('price/add/', price.price_add),
    path('price/<int:nid>/edit/', price.price_edit),
    path('price/<int:nid>/delete/', price.price_delete),
    path('get_price/<int:item_id>/', order.get_price, name='get_price'),

    path('admin/list/', admin.admin_list),
    path('admin/add/', admin.admin_add),
    path('admin/edit/<int:nid>/', admin.admin_edit),
    path('admin/delete/', admin.admin_delete),
    path('admin/reset/<int:nid>/', admin.admin_reset),

    path('login/', index.login),
    path('logout/', index.logout),
    path('index/', index.index),

]
