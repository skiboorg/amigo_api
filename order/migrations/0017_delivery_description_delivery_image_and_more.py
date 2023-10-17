# Generated by Django 4.2.4 on 2023-10-16 19:14

from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0016_order_old_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='delivery',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='WEBP', keep_meta=True, null=True, quality=95, scale=None, size=[400, 300], upload_to='order/delivery'),
        ),
        migrations.AddField(
            model_name='delivery',
            name='is_self_delivery',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='paymenttype',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]