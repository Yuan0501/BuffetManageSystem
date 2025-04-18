from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from app01.utils.bootstrap import BootStrapModelForm, BootStrapForm
from app01 import models
from django import forms

class DepartModelForm(BootStrapModelForm):
    class Meta:
        model = models.Department
        fields = "__all__"

class UserModelForm(forms.ModelForm):
    #name = forms.CharField(min_length=3, label="name")
    class Meta:
        model = models.UserInfo
        fields = ['name', 'password','age', 'account', 'gender', 'department']
        # widgets = {
        #     "name": forms.TextInput(attrs={'class':'form-control', "placeholder":"name"}),
        #     "password": forms.PasswordInput(attrs={'class':'form-control',"placeholder":"password"}),
        #     "age": forms.NumberInput(attrs={'class':'form-control',"placeholder":"age"}),
        #     "account": forms.TextInput(attrs={'class':'form-control',"placeholder":"account"}),
        #     #"create_time": forms.TextInput(attrs={'class':'form-control',"placeholder":"createtime"}),
        #     "gender": forms.Select(attrs={'class':'form-control',"placeholder":"gender"}),
        #     "depart": forms.Select(attrs={'class':'form-control',"placeholder":"department title"}),
        # }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            for name,field in self.fields.items():
                field.widget.attrs={"class":"form-control", "placeholder":field.label}

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


        if 'item' in self.data:
            try:
                item_id = int(self.data.get('item'))
                item = models.Price.objects.get(id=item_id)
                self.fields['price'].initial = item.itemPrice
            except (ValueError, models.Price.DoesNotExist):
                pass

class OrderEditModelForm(forms.ModelForm):


    class Meta:
        model = models.Order
        fields = ["tableNum","serverId", "item","itemNum","status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

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

class AdminModelForm(forms.ModelForm):
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput
    )
    class Meta:
        model = models.Admin
        fields =["username","password","confirm_password"]
        widgets = {
            "password": forms.PasswordInput
        }
    # def clean_password(self):
    #     pwd = self.cleaned_data["password"]
    #
    #     exists = models.Admin.objects.filter(id=self.instance.pk, password=pwd).exists()
    #     if exists:
    #         raise forms.ValidationError("Password can't same as before ones.")
    #     return "999"

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm_password")
        if confirm != pwd:
            raise ValidationError("Passwords don't match")
        return confirm

class AdminEditModelForm(forms.ModelForm):
    class Meta:
        model = models.Admin
        fields = ["username"]

class AdminResetModelForm(forms.ModelForm):
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput
    )
    class Meta:
        model = models.Admin
        fields = ["password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=False)
        }

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm_password")
        if confirm != pwd:
            raise ValidationError("Passwords don't match")
        return confirm

class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        required=True
    )


