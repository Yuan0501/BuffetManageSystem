from django.db import models


class Admin(models.Model):
    """Administration Model"""
    username = models.CharField(verbose_name="UserName", max_length=32)
    password = models.CharField(verbose_name="Password", max_length=64)

class Department(models.Model):
    """部门表"""
    #id = models.AutoField(verbose_name='ID', primary_key=True)
    title = models.CharField(verbose_name='title', max_length=100)

    def __str__(self):
        return self.title

class UserInfo(models.Model):
    """ 员工表"""
    name = models.CharField(verbose_name='Name', max_length=32)
    password = models.CharField(verbose_name='Password', max_length=64)
    age = models.IntegerField(verbose_name='Age')
    account = models.DecimalField(verbose_name='Account', decimal_places=2, max_digits=10, default=0)


    # 无约束
    # depart_id = models。BigIntegerField(verbose_name="Department')

    # 1.有约束
    #  -to， 与哪张表关联
    #  -to_field, 表中哪一列关联
    # 2. django 自动
    #  -写的depart
    #  -生成数据列 depart_id
    # 3. 部门表被删除
    # 3.1 级联删除
    department = models.ForeignKey(to="Department", to_field="id", on_delete=models.CASCADE)
    # 3.2 置空
    #depart = models.ForeignKey(to="Department", to_field="id", null=True, blank=True, on_delete=models.SET。NULL)

    gender_choices = (
        (1, 'male'),
        (2, 'female'),
        (3, 'other'),
    )
    gender = models.SmallIntegerField(verbose_name='Gender', choices=gender_choices)


class Price(models.Model):
    """部门表"""
    #id = models.AutoField(verbose_name='ID', primary_key=True)
    item_choices = (
        (1, "Adult"),
        (2, "Kids 7-10"),
        (3, "kids 3-6"),
        (4, "Iced Tea"),
        (5, "Pepsi"),
        (6, "Lemonade"),
        (7, "Dr Pepper"),
        (8, "Orange Crush"),
        (9, "Big Red"),
        (10, "Hot Tea"),
        (11, "Diet Pepsi"),
        (12, "Coffe"),
    )

    item = models.SmallIntegerField(verbose_name='type', choices=item_choices, default=1)
    itemPrice = models.DecimalField(verbose_name='price',  decimal_places=2, max_digits=10)

    def __str__(self):
        # 返回 item 和 itemPrice 字段的值
        return f"{self.get_item_display()} - {self.itemPrice}"


# class Order(models.Model):
#     """Order Table"""
#     tableNum = models.IntegerField(verbose_name='TableNum')
#     serverId = models.ForeignKey(to="UserInfo", to_field="id", on_delete=models.CASCADE, default=1)
#     item = models.ForeignKey(to="Price", on_delete=models.CASCADE, related_name='orders_as_item')
#     itemNum = models.IntegerField(verbose_name="ItemNumber", default=0)

#     status_choices = (
#         (1, "unpaid"),
#         (2, "paid")
#     )
#     status = models.SmallIntegerField(verbose_name='Status', choices=status_choices, default=1)

