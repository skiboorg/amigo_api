# Generated by Django 4.2.4 on 2023-10-08 06:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_alter_order_total_volume_alter_order_total_weight'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderitem',
            options={'ordering': ('-id',)},
        ),
    ]
