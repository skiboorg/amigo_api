# Generated by Django 4.2.4 on 2023-08-24 11:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('client', '0009_alter_deliveryaddress_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='manager', to=settings.AUTH_USER_MODEL),
        ),
    ]
