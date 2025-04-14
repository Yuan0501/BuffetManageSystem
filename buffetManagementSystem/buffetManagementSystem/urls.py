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
from app01 import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('depart/list/', views.depart_list),
    path('depart/add/', views.depart_add),

    path('depart/delete/', views.depart_delete),
    path('depart/<int:nid>/edit/', views.depart_edit),

    path('user/list/', views.user_list),

    path('user/model/form/add/', views.user_model_form_add),
    path('user/<int:nid>/edit/', views.user_edit),
    path('user/<int:nid>/delete/', views.user_delete),

    path('order/list/', views.order_list),
    path('order/add/', views.order_add),

    path('order/<int:nid>/edit/', views.order_edit),

    path('order/<int:nid>/delete/', views.order_delete),
    path('price/list/', views.price_list),
    path('price/add/', views.price_add),

    path('price/<int:nid>/edit/', views.price_edit),

    path('price/<int:nid>/delete/', views.price_delete),

    path('get_price/<int:item_id>/', views.get_price, name='get_price'),

    path('admin/list/', views.admin_list),
    path('admin/add/', views.admin_add),
    path('admin/edit/<int:nid>/', views.admin_edit),
    path('admin/delete/<int:nid>/', views.admin_delete),
    path('admin/reset/<int:nid>/', views.admin_reset),
    path('login/', views.login),
    path('logout/', views.logout),
    path('index/', views.index),

]

