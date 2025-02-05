# Generated by Django 5.1.5 on 2025-01-26 22:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_cart_is_paid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='product',
        ),
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
