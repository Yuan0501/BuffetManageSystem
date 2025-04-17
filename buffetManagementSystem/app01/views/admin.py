from django.shortcuts import render, redirect
from django.http import JsonResponse
from app01.models import Price
import json
from django.views.decorators.csrf import csrf_exempt
from app01 import models
from django.core.paginator import Paginator
from app01.utils.form import AdminModelForm, AdminEditModelForm, AdminResetModelForm

def admin_list(request):
    """admin list"""

    info = request.session.get('info')
    if not info:
        return redirect('/login/')

    queryset = models.Admin.objects.all()


    # context = {
    #     'queryset': queryset,
    # }
    return render(request, 'admin_list.html', {"queryset":queryset})

def admin_add(request):
    """admin add"""
    title = "New Admin"
    if request.method == 'GET':
        form = AdminModelForm()
        return render(request,'change.html',{'form':form,"title": title})
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'change.html', {'form': form, "title": title})

def admin_edit(request, nid):
    """admin edit"""

    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect('/admin/list/')

    title = "Edit Admin"

    if request.method == 'GET':
        form = AdminEditModelForm(instance=row_object)
        return render(request, 'change.html', {"form":form, "title": title})

    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'change.html', {'form': form, "title": title})

def admin_delete(request):
    """admin delete"""
    uid = request.GET.get('uid')
    exists = models.Admin.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status":False,'error': "Data is not exist"})

    models.Admin.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})

def admin_reset(request, nid):
    """admin reset"""
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect('/admin/list/')
    title = "Reset Password - {}".format(row_object.username)
    if request.method == 'GET':
        form = AdminResetModelForm()
        return render(request, 'change.html', {'form': form, "title": title})
    form = AdminResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'change.html', {'form': form, "title": title})
