# Generated by Django 4.2.4 on 2023-09-26 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_alter_order_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='totalPrice',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='totalPrice',
        ),
        migrations.AddField(
            model_name='order',
            name='amount',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='total_volume',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=6, null=True, verbose_name='Общий Объем, m3'),
        ),
        migrations.AddField(
            model_name='order',
            name='total_weight',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=6, null=True, verbose_name='Общий Вес, кг'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='price_with_discount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, null=True, verbose_name='Стоимость со скидкой'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=13, null=True, verbose_name='Общий Стоимость'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='total_volume',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=6, null=True, verbose_name='Общий Объем, m3'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='total_weight',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=6, null=True, verbose_name='Общий Вес, кг'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=16, null=True, verbose_name='Общий Стоимость'),
        ),
    ]
