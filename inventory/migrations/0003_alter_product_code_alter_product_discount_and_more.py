# Generated by Django 4.2.17 on 2025-01-16 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_product_code_alter_product_cost_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='code',
            field=models.CharField(default='1', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Percentage discount', max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='sales_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
