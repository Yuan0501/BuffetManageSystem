# Generated by Django 5.1.7 on 2025-04-10 18:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.SmallIntegerField(choices=[(1, 'Adult'), (2, 'Kids 7-10'), (3, 'kids 3-6'), (4, 'Iced Tea'), (5, 'Pepsi'), (6, 'Lemonade'), (7, 'Dr Pepper'), (8, 'Orange Crush'), (9, 'Big Red'), (10, 'Hot Tea'), (11, 'Diet Pepsi'), (12, 'Coffe')], default=1, verbose_name='type')),
                ('itemPrice', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='price')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tableNum', models.IntegerField(verbose_name='TableNum')),
                ('itemNum', models.IntegerField(default=0, verbose_name='ItemNumber')),
                ('status', models.SmallIntegerField(choices=[(1, 'unpaid'), (2, 'paid')], default=1, verbose_name='Status')),
                ('serverId', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app01.userinfo')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders_as_item', to='app01.price')),
            ],
        ),
    ]
