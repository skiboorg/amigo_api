# Generated by Django 4.2.4 on 2023-10-01 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0012_alter_client_options_alter_note_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='note',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]