# Generated by Django 4.2.4 on 2023-08-02 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0007_alter_note_created_at_alter_note_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='note_old_type',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Тип из старой базы'),
        ),
    ]
