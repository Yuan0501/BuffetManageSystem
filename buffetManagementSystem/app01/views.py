from django.shortcuts import render, redirect
from django.template.defaultfilters import title

from app01 import models
from django.http import JsonResponse
from app01.models import Price

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

def order_list(request):
    """order list"""
    data_dict = {}
    search_data = request.GET.get('q',"")
    if search_data:
        data_dict["tableNum"] = search_data

    queryset = models.Order.objects.filter(**data_dict).order_by("id")

    return render(request, 'order_list.html', {"queryset":queryset, "search_data":search_data})


class OrderModelForm(forms.ModelForm):
    # 使用 ModelChoiceField 来实现 item 下拉选择
    item = forms.ModelChoiceField(
        queryset=models.Price.objects.all(),
        empty_label="Select Item",  # 下拉列表中的默认选项
        widget=forms.Select(attrs={'class': 'form-control'})  # 添加样式
    )

    # price 字段应该显示选择的 item 的价格，而不是另一个下拉框
    price = forms.DecimalField(
        label="Price",
        max_digits=10,
        decimal_places=2,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )

    class Meta:
        model = models.Order
        fields = ['tableNum','serverId', 'item', 'itemNum', 'price', 'status']  # 只选择相关字段

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control", "placeholder": field.label})

        # 当选择 item 时，自动填充 price
        if 'item' in self.data:
            try:
                item_id = int(self.data.get('item'))
                item = models.Price.objects.get(id=item_id)
                self.fields['price'].initial = item.itemPrice
            except (ValueError, models.Price.DoesNotExist):
                pass


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

class OrderEditModelForm(forms.ModelForm):


    class Meta:
        model = models.Order
        fields = ["tableNum","serverId", "item","itemNum","status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


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

class PriceModelForm(forms.ModelForm):
    # mobile = forms.CharField(
    #     label="Mobile",
    #     validators=[RegexValidator(r'\d{10}$', 'mobile must be 10 digit numbers')],
    # )
    class Meta:
        model = models.Price
        # fields = ["mobile","price","level","status"]
        # exclude = ['level]
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


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

class PriceEditModelForm(forms.ModelForm):


    class Meta:
        model = models.Price
        fields = ["item","itemPrice"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    # def clean_mobile(self):
    #
    #
    #     txt_mobile = self.cleaned_data['mobile']
    #
    #     exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
    #     if exists:
    #         raise ValidationError("Mobile number already exists")
    #
    #     else:
    #         return txt_mobile

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
