# Generated by Django 4.2.17 on 2025-01-31 00:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0007_payment_amount_paid_payment_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_dt',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
