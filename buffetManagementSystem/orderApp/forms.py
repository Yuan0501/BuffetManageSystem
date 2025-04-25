from django import forms
from django.db.models.base import Model
from orderApp.models import Order_new, OrderItem
from django.forms import inlineformset_factory
from app01.models import UserInfo

class UserInfoChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class OrderForm(forms.ModelForm):
    server = UserInfoChoiceField(
        queryset=UserInfo.objects.all(),
        label="Server Name",
        widget=forms.Select(attrs={
            'class': 'form-control w-auto',
            'id': 'serverSelect',
        })
    )

    class Meta:
        model = Order_new
        fields = ['tableNum','server']
        widgets = {
            'tableNum':forms.NumberInput(attrs={
                'class': 'form-control w-auto',
                'min':1,
                'id': 'tableNumInput',
                }),
        }



class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['item']
        widgets = {
            'item': forms.Select(attrs={'class':'form-control item-select'})
        }


OrderItemFormSet = inlineformset_factory(
    Order_new,
    OrderItem,
    form=OrderItemForm,
    extra=1,
    can_delete=True
)