# Generated by Django 4.2.17 on 2025-01-16 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_remove_payment_payment_dt_alter_payment_payment_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='sub_total',
            field=models.DecimalField(decimal_places=2, max_digits=7, null=True),
        ),
    ]
