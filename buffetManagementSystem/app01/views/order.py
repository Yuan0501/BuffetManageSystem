from django.shortcuts import render, redirect
from django.http import JsonResponse
from app01.models import Price
from app01 import models
from django.core.paginator import Paginator
from app01.utils.form import OrderModelForm, OrderEditModelForm


def order_list(request):
    # """order list"""
    search_data = request.GET.get("q", "")
    queryset = models.Order.objects.all()
    if search_data:
        queryset = queryset.filter(tableNum__contains=search_data)

    paginator = Paginator(queryset, 10)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)

    return render(request, 'order_list.html', {
        "queryset": page_obj,
        "search_data": search_data
    })

def order_add(request):
    """Order form add"""
    if request.method == 'GET':
        form = OrderModelForm()
        return render(request, 'order_add.html', {"form": form})

    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        form.save()  # The form already has the correct Price instance assigned to `price`.
        return redirect("/order/list")
    else:
        return render(request, 'order_add.html', {"form": form})

def get_price(request, item_id):
    try:
        item = Price.objects.get(id=item_id)
        return JsonResponse({'price': str(item.itemPrice)})
    except Price.DoesNotExist:
        return JsonResponse({'price': ''})

def order_edit(request,nid):
    """pretty form edit"""
    row_object = models.Order.objects.filter(id=nid).first()

    if request.method == 'GET':
        form = OrderEditModelForm(instance=row_object)
        return render(request,'order_edit.html',{"form":form})
    form = OrderEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/order/list/')
    else:
        return render(request,'order_edit.html', {"form": form})

def order_delete(request):
    """order form delete"""
    uid = request.GET.get('uid')
    exists = models.Order.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": False, 'error': "Data is not exist"})

    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})


