# Generated by Django 4.2.4 on 2023-09-14 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_product_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('slug', models.CharField(blank=True, help_text='Если не заполнено, создается на основе поля Назавание', max_length=255, null=True, verbose_name='ЧПУ')),
                ('categories', models.ManyToManyField(related_name='filters', to='product.productcategory')),
            ],
            options={
                'verbose_name': 'Фильтр',
                'verbose_name_plural': 'Фильтры',
            },
        ),
        migrations.RemoveField(
            model_name='product',
            name='subCategory',
        ),
        migrations.AddField(
            model_name='product',
            name='isDiscount',
            field=models.BooleanField(default=True, verbose_name='Товар новинка?'),
        ),
        migrations.AddField(
            model_name='product',
            name='isNew',
            field=models.BooleanField(default=True, verbose_name='Товар новинка?'),
        ),
        migrations.AddField(
            model_name='productprice',
            name='isActive',
            field=models.BooleanField(default=True, verbose_name='Отображать?'),
        ),
        migrations.AddField(
            model_name='productprice',
            name='vendorCode',
            field=models.CharField(max_length=255, null=True, verbose_name='Артикул'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.productcategory'),
        ),
        migrations.DeleteModel(
            name='ProductSubCategory',
        ),
        migrations.AddField(
            model_name='product',
            name='filters',
            field=models.ManyToManyField(to='product.filter'),
        ),
    ]