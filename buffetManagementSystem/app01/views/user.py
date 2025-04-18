from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from app01.models import Price
import json
from django.views.decorators.csrf import csrf_exempt
from app01 import models
from django.core.paginator import Paginator
from app01.utils.form import  UserModelForm
from app01.utils.form import DepartModelForm

def user_list(request):
    """user list"""

    queryset = models.UserInfo.objects.all()
    form = UserModelForm()
    return render(request, 'user_list.html',{'form':form, "queryset":queryset})

@csrf_exempt
def user_add(request):
    """user model form add"""
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})

    return JsonResponse({"status": False, 'error': form.errors})

def user_delete(request):
    uid = request.GET.get('uid')
    exists = models.UserInfo.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": False, 'error': "Data is not exist"})

    models.UserInfo.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})

@csrf_exempt
def user_edit(request):
    """user edit"""
    uid = request.GET.get('uid')
    row_object = models.UserInfo.objects.filter(id=uid).first()
    print(row_object)
    if not row_object:
        return JsonResponse({"status": False, 'tips': "Data is not exist"})

    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})

def user_detail(request):
    uid = request.GET.get('uid')
    row_dict = models.UserInfo.objects.filter(id=uid).values("id", "name", "password", "age", "account", "gender", "department").first()
    if not row_dict:
        return JsonResponse({"status": False, 'error': "Data is not exist"})
    result = {
        "status": True,
        "data": row_dict
    }
    return JsonResponse(result)
