from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from app01 import models
from app01.utils.form import DepartModelForm

def depart_list(request):
    """Department list"""
    queryset = models.Department.objects.all()
    form=DepartModelForm()
    return render(request, 'depart_list.html', {'form': form,'queryset': queryset})

@csrf_exempt
def depart_add(request):
    """Department add"""
    form = DepartModelForm(data=request.POST)
    if form.is_valid():

        # 额外增加一些不是用户输入的值（自己计算出来）
        # form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S) + str(random.randint(1000,9999)

        # 固定设置管理员ID

        # form.instance.admin_id = request.session["info"]["id"] #当前登录系统管理员的ID
        form.save()
        return JsonResponse({"status": True})

    return JsonResponse({"status": False, 'error': form.errors})

def depart_delete(request):
    """department delete"""
    # # 获取ID
    # nid = request.GET.get('nid')
    # # 删除
    # models.Department.objects.filter(id=nid).delete()
    # # 重定向回部门列表
    # return redirect("/depart/list")

    uid = request.GET.get('uid')
    exists = models.Department.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status":False,'error': "Data is not exist"})

    models.Department.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})

@csrf_exempt
def depart_edit(request):
    """department edit"""
    uid = request.GET.get('uid')
    row_object = models.Department.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status":False,'tips': "Data is not exist"})

    form = DepartModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})

def depart_detail(request):
    # uid = request.GET.get('uid')
    # row_object = models.Department.objects.filter(id=uid).first()
    # if not row_object:
    #     return JsonResponse({"status":False,'error': "Data is not exist"})
    # result = {
    #     "status": True,
    #     "data": {
    #         "title": row_object.title,
    #     }
    #
    # }
    # return JsonResponse({result})
    uid = request.GET.get('uid')
    row_dict = models.Department.objects.filter(id=uid).values("title").first()
    if not row_dict:
        return JsonResponse({"status":False,'error': "Data is not exist"})
    result = {
        "status": True,
        "data": row_dict
     }
    return JsonResponse(result)
