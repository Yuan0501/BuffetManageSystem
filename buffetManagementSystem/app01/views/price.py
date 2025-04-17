from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from app01.models import Price
import json
from django.views.decorators.csrf import csrf_exempt
from app01 import models
from django.core.paginator import Paginator
from app01.utils.form import PriceModelForm, PriceEditModelForm



def price_list(request):
    """price list"""

    data_dict = {}
    search_data = request.GET.get('q',"")
    if search_data:
        data_dict["item__in"] = [
            price[0] for price in models.Price.item_choices
            if search_data.lower() in price[1].lower()  # 匹配输入的字符串
        ]

    queryset = models.Price.objects.filter(**data_dict).order_by("id")

    return render(request, 'price_list.html', {"queryset":queryset, "search_data":search_data})

def price_add(request):
    """price form add"""
    if request.method == 'GET':
        form = PriceModelForm()
        return render(request,'price_add.html',{"form":form})
    form = PriceModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/price/list")
        #print(form.cleaned_data)
    else:
        return render(request,'price_add.html',{"form":form})

def price_edit(request,nid):
    """pretty form edit"""
    row_object = models.Price.objects.filter(id=nid).first()

    if request.method == 'GET':
        form = PriceEditModelForm(instance=row_object)
        return render(request,'price_edit.html',{"form":form})
    form = PriceEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/price/list/')
    else:
        return render(request,'price_edit.html', {"form": form})

def price_delete(request, nid):
    """price form delete"""
    models.Price.objects.filter(id=nid).delete()
    return redirect('/price/list/')