from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from app01.models import Price
import json
from django.views.decorators.csrf import csrf_exempt
from app01 import models
from django.core.paginator import Paginator
from app01.utils.form import  UserModelForm



def user_list(request):
    """user list"""

    queryset = models.UserInfo.objects.all()

        # obj.depart_id 获取数据库中存储的那个字段
        # obj.depart.title 根据id自动去关联的表中获取哪一行数据depart对象
    return render(request, 'user_list.html',{"queryset":queryset})

def user_add(request):
    """user add"""
    if request.method == 'GET':

        context = {
            'gender_choices': models.UserInfo.gender_choices,
            'depart_lists': models.Department.objects.all()
        }
        return render(request, 'user_add.html',context)

    name = request.POST.get('name')
    pwd = request.POST.get('pwd')
    age = request.POST.get('age')
    account = request.POST.get('ac')
    ctime =request.POST.get('ctime')
    gender = request.POST.get('gd')
    department_id = request.POST.get('dp')

    models.UserInfo.objects.create(name=name, password=pwd, age=age, account=account, gender=gender, department_id=department_id)

    return redirect("/user/list")

def user_model_form_add(request):
    """user model form add"""
    if request.method == 'GET':
        form = UserModelForm()
        return render(request,'user_model_form_add.html',{"form":form})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/user/list")
        #print(form.cleaned_data)
    else:
        return render(request,'user_model_form_add.html',{"form":form})