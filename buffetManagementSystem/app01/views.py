from django.shortcuts import render, redirect
from django.template.defaultfilters import title

from app01 import models

def depart_list(request):
    """Department list"""

    queryset = models.Department.objects.all()

    return render(request, 'depart_list.html', {'queryset': queryset})

def depart_add(request):
    """Department add"""
    if request.method == 'GET':
        return render(request, 'depart_add.html')

    # 获取用户POST提交过来的数据 (title输入为空）
    tit = request.POST.get("title")

    # 保存到数据库
    models.Department.objects.create(title=tit)

    # 重定向回不萌列表
    return redirect("/depart/list")

def depart_delete(request):
    """department delete"""
    # 获取ID
    nid = request.GET.get('nid')
    # 删除
    models.Department.objects.filter(id=nid).delete()
    # 重定向回部门列表
    return redirect("/depart/list")

def depart_edit(request, nid):
    """department edit"""
    # 根据nid,获取他的数据[obj.]
    if request.method == 'GET':
        row_object = models.Department.objects.filter(id=nid).first()
        return render(request,'depart_edit.html', {'row_object':row_object})

    # 根据ID找到数据库中的数据并更新

    title = request.POST.get("title")
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect("/depart/list")

def user_list(request):
    """user list"""
    queryset = models.UserInfo.objects.all()
    for obj in queryset:
        print(obj.id, obj.name, obj.account, obj.get_gender_display(), obj.department.title)
        # obj.depart_id 获取数据库中存储的那个字段
        # obj.depart.title 根据id自动去关联的表中获取哪一行数据depart对象
    return render(request, 'user_list.html',{"queryset":queryset})


from django import forms

class UserModelForm(forms.ModelForm):
    #name = forms.CharField(min_length=3, label="name")
    class Meta:
        model = models.UserInfo
        fields = ['name', 'password','age', 'account', 'gender', 'department']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

def user_model_form_add(request):
    """user model form add"""
    if request.method == 'GET':
        form = UserModelForm()
        return render(request,'user_model_form_add.html',{"form":form})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/user/list")
    else:
        return render(request,'user_model_form_add.html',{"form":form})

def user_edit(request,nid):
    """user edit"""
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = UserModelForm(instance=row_object)
        return render(request,'user_edit.html', {"form": form})

    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    else:
        return render(request,'user_edit.html', {"form": form})

def user_delete(request,nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list")