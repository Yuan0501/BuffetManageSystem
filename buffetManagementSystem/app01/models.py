from django.db import models

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




