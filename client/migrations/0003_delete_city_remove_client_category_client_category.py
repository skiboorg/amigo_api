# Generated by Django 4.2.4 on 2023-08-02 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='City',
        ),
        migrations.RemoveField(
            model_name='client',
            name='category',
        ),
        migrations.AddField(
            model_name='client',
            name='category',
            field=models.ManyToManyField(null=True, to='client.category'),
        ),
    ]
