# Generated by Django 4.2.4 on 2023-08-02 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_delete_city_remove_client_category_client_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='created_at',
            field=models.DateField(null=True),
        ),
    ]
