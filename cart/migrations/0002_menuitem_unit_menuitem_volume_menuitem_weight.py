# Generated by Django 4.2.17 on 2025-01-16 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='unit',
            field=models.CharField(blank=True, default='piece', help_text='Unit of measurement (e.g., piece, plate, pair)', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='volume',
            field=models.DecimalField(blank=True, decimal_places=2, default=1, help_text='Volume in liters (e.g., 1.0 L)', max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=2, default=1, help_text='Weight in grams (e.g., 500g)', max_digits=10, null=True),
        ),
    ]
