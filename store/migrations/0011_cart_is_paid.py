# Generated by Django 5.1.5 on 2025-01-26 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_alter_cartitem_cart_alter_cartitem_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
    ]
