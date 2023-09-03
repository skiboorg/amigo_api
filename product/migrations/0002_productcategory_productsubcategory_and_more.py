# Generated by Django 4.2.4 on 2023-09-03 16:01

from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('image', django_resized.forms.ResizedImageField(crop=None, force_format='WEBP', keep_meta=True, null=True, quality=95, scale=None, size=[420, 420], upload_to='product/gallery')),
                ('slug', models.CharField(blank=True, help_text='Если не заполнено, создается на основе поля Назавание', max_length=255, null=True, verbose_name='ЧПУ')),
            ],
            options={
                'verbose_name': 'Категория товара',
                'verbose_name_plural': 'Категории товаров',
            },
        ),
        migrations.CreateModel(
            name='ProductSubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('slug', models.CharField(blank=True, help_text='Если не заполнено, создается на основе поля Назавание', max_length=255, null=True, verbose_name='ЧПУ')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_categories', to='product.productcategory')),
            ],
            options={
                'verbose_name': 'Подкатегория товара',
                'verbose_name_plural': 'Подкатегория товаров',
            },
        ),
        migrations.RemoveField(
            model_name='product',
            name='productType',
        ),
        migrations.DeleteModel(
            name='ProductType',
        ),
        migrations.AddField(
            model_name='product',
            name='subCategory',
            field=models.ManyToManyField(blank=True, to='product.productsubcategory'),
        ),
    ]
