# Generated by Django 4.2.4 on 2023-10-17 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_productcategory_old_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='isDiscount',
            field=models.BooleanField(default=False, verbose_name='Товар со скидкой?'),
        ),
    ]
