# Generated by Django 5.1.5 on 2025-01-25 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('paid', 'Paid'), ('completed', 'Completed')], default='pending', max_length=10),
        ),
    ]
