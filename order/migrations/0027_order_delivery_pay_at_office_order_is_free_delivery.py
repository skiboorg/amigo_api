# Generated by Django 4.2.4 on 2023-10-27 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0026_order_is_pay_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_pay_at_office',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='is_free_delivery',
            field=models.BooleanField(default=False),
        ),
    ]
