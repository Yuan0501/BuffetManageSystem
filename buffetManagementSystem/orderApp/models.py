from django.db import models
from app01.models import UserInfo, Price
from decimal import Decimal
from django.db.models import Sum, DecimalField

# Create your models here.
class Order_new(models.Model):
    """Order Table"""
    tableNum = models.IntegerField(verbose_name='TableNum')
    server = models.ForeignKey(UserInfo, on_delete=models.CASCADE, default=1)
    order_time = models.DateTimeField("OderDate", auto_now_add=True)
    total_price = models.DecimalField(verbose_name='TotalPrice', decimal_places=2, max_digits=10, default=0)
    
    def update_total_price(self):
        agg = self.order_items.aggregate(total=Sum('unit_price', output_field=DecimalField()))
        self.total_price = agg['total'] or Decimal('0')
        self.save(update_fields=['total_price'])
    
    @property
    def compute_total_price(self):
        agg = self.order_items.aggregate(total=Sum('unit_price', output_field=DecimalField()))
        return agg['total'] or Decimal('0')




class OrderItem(models.Model):
    """Order Item Table"""
    order = models.ForeignKey(Order_new, on_delete=models.CASCADE, related_name='order_items',verbose_name='OrderItem')
    item = models.ForeignKey(Price, on_delete=models.CASCADE, related_name='orders_as_item')
    unit_price = models.DecimalField(verbose_name='UnitPrice', decimal_places=2, max_digits=10)

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
    
    def save(self, *args, **kwargs):
        # Calculate the unit price based on the related Price instance
        self.unit_price = self.item.itemPrice
        super().save(*args, **kwargs)
        self.order.update_total_price()