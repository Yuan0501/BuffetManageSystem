from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from orderApp.models import Order_new, OrderItem
from orderApp.forms import OrderForm, OrderItemFormSet
from django.views import View
from django.views.generic import ListView
from app01.models import Price
from django.views.decorators.http import require_POST




class OrderListView(ListView):
    model =  Order_new
    template_name = 'orderApp/order_list.html'
    context_object_name = 'orders'


class OrderCreateView(View):
    def get(self, request):
        form = OrderForm()
        formset = OrderItemFormSet(prefix='form')
        prices = Price.objects.all()
        return render(request, 'orderApp/order_form.html',{
            'form': form,
            'formset': formset,
            'prices': prices
        })
    
    def post(self, request):
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.serverId = request.user  # Assuming you have a user logged in
            order.save()
            formset = OrderItemFormSet(request.POST, instance=order, prefix='form')
            if formset.is_valid():
                formset.save()
                order.update_total_price()
                return redirect('order_list')
        
        prices = Price.objects.all()
        formset = OrderItemFormSet(request.POST, prefix='form')
        return render(request,'orderApp/order_form.html',{
            'form': form,
            'formset': formset,
            'prices': prices
        })

@require_POST
def add_price(request):
    name = request.POST.get('name')
    price = request.POST.get('price')
    if not name or not price:
        return  JsonResponse({'status': 400, 'error': 'Name and price are required.'})
    p = Price.objects.create(itemName=name, itemPrice=price)
    return JsonResponse({
        'id': p.id,
        'name': p.itemName,
        'price': str(p.itemPrice)
    })
    
