# Generated by Django 4.2.4 on 2023-09-06 09:57

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Название')),
                ('slug', models.CharField(max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Категория блога',
                'verbose_name_plural': 'Категории блога',
            },
        ),
        migrations.CreateModel(
            name='BlogItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Название')),
                ('slug', models.CharField(max_length=255, null=True)),
                ('shortDescription', models.TextField(blank=True, null=True, verbose_name='Короткое описание')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Контент')),
                ('image', django_resized.forms.ResizedImageField(crop=None, force_format='WEBP', keep_meta=True, null=True, quality=95, scale=None, size=[800, 450], upload_to='blog')),
                ('is_news_item', models.BooleanField(default=True, verbose_name='Это новость?')),
                ('readTime', models.CharField(max_length=255, null=True, verbose_name='Время прочтения')),
                ('createdAt', models.DateField(blank=True, null=True, verbose_name='Дата')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='data.blogcategory')),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
            },
        ),
    ]
