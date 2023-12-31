# Generated by Django 4.2.4 on 2023-09-29 07:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0012_alter_client_options_alter_note_priority'),
        ('order', '0008_alter_orderitem_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='client.client'),
        ),
    ]
