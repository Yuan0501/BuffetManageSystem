from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from app01 import models
from django.core.paginator import Paginator
from app01.utils.form import PriceModelForm, PriceEditModelForm



# def price_list(request):
#     """price list"""
#     search_data = request.GET.get("q", "")
#     queryset = models.Price.objects.all()
#     if search_data:
#         queryset = queryset.filter(item__contains=search_data)
#
#     paginator = Paginator(queryset, 10)  # 每页 10 条
#     page = request.GET.get("page")
#     page_obj = paginator.get_page(page)
#
#     return render(request, 'price_list.html', {
#         "queryset": page_obj,
#         "search_data": search_data
#     })

    # data_dict = {}
    # search_data = request.GET.get('q',"")
    # if search_data:
    #     data_dict["item__in"] = [
    #         price[0] for price in models.Price.item_choices
    #         if search_data.lower() in price[1].lower()  # 匹配输入的字符串
    #     ]
    #
    # queryset = models.Price.objects.filter(**data_dict).order_by("id")
    #
    # return render(request, 'price_list.html', {"queryset":queryset, "search_data":search_data})

def price_list(request):
    """price list"""
    search_data = request.GET.get("q", "")
    queryset = models.Price.objects.all()

    if search_data:
        # 通过 item_choices 来查找匹配的整数值
        item_dict = dict(models.Price.item_choices)
        item_value = None

        # 搜索对应名称的项
        for key, value in item_dict.items():
            if value.lower() == search_data.lower():  # 匹配名称
                item_value = key
                break

        if item_value is not None:
            queryset = queryset.filter(item=item_value)

    paginator = Paginator(queryset, 10)  # 每页 10 条
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)

    return render(request, 'price_list.html', {
        "queryset": page_obj,
        "search_data": search_data
    })

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

def price_delete(request):
    """price form delete"""
    uid = request.GET.get('uid')
    exists = models.Price.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": False, 'error': "Data is not exist"})

    models.Price.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})