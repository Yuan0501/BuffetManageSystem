from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from app01.models import Price
import json
from django.views.decorators.csrf import csrf_exempt
from app01 import models
from django.core.paginator import Paginator
from app01.utils.form import OrderModelForm, OrderEditModelForm


def order_list(request):
    # """order list"""
    search_data = request.GET.get("q", "")
    queryset = models.Order.objects.all()
    if search_data:
        queryset = queryset.filter(tableNum__contains=search_data)

    paginator = Paginator(queryset, 10)  # 每页 10 条
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)

    return render(request, 'order_list.html', {
        "queryset": page_obj,  # 注意：这里要传的是 page_obj
        "search_data": search_data
    })

    #
    # data_dict = {}
    # search_data = request.GET.get('q',"")
    # if search_data:
    #     data_dict["tableNum"] = search_data
    #
    #
    # page = int(request.GET.get('page', 1))
    # page_size = 10
    # start = (page - 1) * page_size
    # end = start * page_size
    #
    #
    # queryset = models.Order.objects.filter(**data_dict).order_by("id")[start:end]
    # total_count = models.Order.objects.filter(**data_dict).order_by("id").count()
    # total_page_count, div = divmod(total_count, page_size)
    # if div:
    #     total_page_count += 1
    #     plus = 5
    #     if total_page_count <= 2 * plus + 1:
    #         start_page = 1
    #         end_page = total_page_count
    #     else:
    #         if page <= plus:
    #             start_page = 1
    #             end_page = 2 * plus + 1
    #         else:
    #             if (page + plus) > total_page_count:
    #                 start_page = total_page_count - 2 * plus
    #                 end_page = total_page_count
    #             else:
    #                 start_page = page - plus
    #                 end_page = page + plus
    #
    # page_str_list = []
    # page_str_list.append('<li><a href="page={}">First</a></li>').format(1)
    # if page > 1:
    #     prev = '<li><a href="page={}">Previous</a></li>'.format(page - 1)
    # else:
    #     prev = '<li><a href="page={}">Previous</a></li>'.format(1)
    # page_str_list.append(prev)
    # for i in range(start_page, end_page + 1):
    #     if i == page:
    #         ele = '<li class="active"><a href="page={}"><{}/a></li>'.format(i,i)
    #     else:
    #         ele = '<li><a href="page={}">{}</a></li>'.format(i, i)
    #     page_str_list.append(ele)
    # if page < total_page_count:
    #     prev = '<li><a href="page={}">Next</a></li>'.format(page + 1)
    # else:
    #     prev = '<li><a href="page={}">Next</a></li>'.format(total_page_count)
    # page_str_list.append(prev)
    # page_str_list.append('<li><a href="page={}">Last</a></li>').format(total_page_count)
    # page_string = mark_safe("".join(page_str_list))
    #
    #
    # return render(request, 'order_list.html', {"queryset":queryset, "search_data":search_data})
    #


def order_add(request):
    """Order form add"""
    if request.method == 'GET':
        form = OrderModelForm()
        return render(request, 'order_add.html', {"form": form})

    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
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

def order_delete(request, nid):
    """order form delete"""
    models.Order.objects.filter(id=nid).delete()
    return redirect('/order/list/')
