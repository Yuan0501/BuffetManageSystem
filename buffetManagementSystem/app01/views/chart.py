from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.db.models import Sum
from django.db.models.functions import TruncDate
from orderApp.models import Order_new
from orderApp import models as order_models
import json
from django.views.decorators.csrf import csrf_exempt
from app01 import models
from django.core.paginator import Paginator
from datetime import datetime
from django.db.models.functions import TruncDate
from django.db.models import Sum
from django.shortcuts import render
from orderApp.models import Order_new
from django.db.models import Sum
from datetime import datetime
from django.shortcuts import render
from django.db.models.functions import ExtractHour

def chart_list(request):
    # 获取两个不同的日期筛选参数
    date_filter = request.GET.get('date')
    graph_filter = request.GET.get('graph_date')

    # 获取所有订单（或按日期过滤）
    sales_data = Order_new.objects.all()
    bar_data = Order_new.objects.all()

    # 日期格式正确性处理
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            sales_data = sales_data.filter(order_time__date=filter_date)
        except ValueError:
            pass

    if graph_filter:
        try:
            graph_date = datetime.strptime(graph_filter, '%Y-%m-%d').date()
            bar_data = bar_data.filter(order_time__date=graph_date)
        except ValueError:
            pass

    # Server sales 数据
    data = sales_data.values('server__name').annotate(sales=Sum('total_price'))

    # Bar graph 数据（按小时汇总）
    hourly_sales = (
        bar_data.annotate(hour=ExtractHour('order_time'))
        .values('hour')
        .annotate(sales=Sum('total_price'))
        .order_by('hour')
    )

    # Convert 'sales' to float before rendering
    hourly_sales = [
        {'hour': item['hour'], 'sales': float(item['sales']) if item['sales'] is not None else 0.0}
        for item in hourly_sales
    ]

    # 所有订单的唯一日期（用于下拉列表）
    order_dates = Order_new.objects.dates('order_time', 'day')
    graph_dates = order_dates  # 同样日期来源

    return render(request, 'chart_list.html', {
        'data': data,
        'order_dates': order_dates,
        'graph_dates': graph_dates,
        'date_filter': date_filter,
        'graph_filter': graph_filter,
        'bar_data': list(hourly_sales),  # Ensure 'bar_data' is passed as a list
    })

