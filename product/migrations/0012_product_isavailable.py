# Generated by Django 4.2.4 on 2023-10-09 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_remove_feedback_avatar_remove_feedback_tour'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='isAvailable',
            field=models.BooleanField(default=True, verbose_name='В наличии?'),
        ),
    ]
