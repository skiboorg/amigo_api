# Generated by Django 4.2.4 on 2023-10-05 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_alter_order_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='total_volume',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=9, null=True, verbose_name='Общий Объем, m3'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='total_weight',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=9, null=True, verbose_name='Общий Вес, кг'),
        ),
    ]
