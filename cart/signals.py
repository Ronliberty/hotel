from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, OrderItem

@receiver(post_save, sender=Order)
def deduct_stock_on_payment(sender, instance, **kwargs):
    """Deduct counter stock when an order is marked as paid."""
    if instance.status == "paid":  # Ensure stock is deducted only when payment is confirmed
        order_items = OrderItem.objects.filter(order=instance)
        for item in order_items:
            try:
                item.deduct_stock()  # ✅ Use the model method instead of duplicating logic
            except ValueError as e:
                print(str(e))  # Handle cases where stock is insufficient
