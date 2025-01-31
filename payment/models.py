from django.db import models
from django.conf import settings
from django.utils import timezone
from cart.models import Order


class Payment(models.Model):
    """
    Represents payment details for an order in the hotel system.

    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    date_time = models.DateTimeField(auto_now_add=True)
    payment_dt = models.DateTimeField(default=timezone.now, blank=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        null=False,
        blank=False,
        editable=False
    )
    payment_id = models.CharField(unique=True, max_length=50, editable=True, null=False)
    total_payment = models.DecimalField(max_digits=10, decimal_places=2, null=False, editable=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0.00, editable=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0.00, editable=False)
    sub_total = models.DecimalField(max_digits=7, decimal_places=2, null=True, editable=True)
    tax_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, editable=True)
    payment_type = models.CharField(
        choices=[('CASH', 'CASH'), ('CARD', 'CARD'), ('MOBILE', 'MOBILE')],
        max_length=32,
        null=False,
        editable=True
    )
    served_by = models.CharField(max_length=100, null=True, blank=True, help_text="Staff or cashier handling the transaction")

    def __str__(self):
        return f"Payment {self.payment_id} - {self.total_payment} ({self.payment_type})"

    def save(self, *args, **kwargs):
        """
        Override save method to calculate balance and update order status correctly.
        """
        # Calculate balance (handle overpayments properly)
        self.balance = max(self.total_payment - self.amount_paid, 0)

        # Determine order status based on payments
        total_paid = sum(payment.amount_paid for payment in self.order.payments.all()) + self.amount_paid
        if total_paid >= self.total_payment:
            self.order.status = 'paid'
        else:
            self.order.status = 'partial'  # New status for incomplete payments

        super().save(*args, **kwargs)  # Save the payment first
        self.order.save()  # Update order status

    class Meta:
        verbose_name_plural = "Payments"


class PaymentOrder(models.Model):
    """
    Tracks the order and payment relationship in the hotel system.
    """
    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name='payment_orders',
        null=False,
        blank=False,
        editable=False
    )
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='payment_order',
        null=False,
        blank=False
    )
    name = models.CharField(max_length=125, editable=False, blank=True, null=True)
    cost_price = models.DecimalField(max_digits=7, decimal_places=2, editable=False, default=0, null=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, null=False, editable=False, help_text="Amount paid in Ksh")
    tax_applied = models.DecimalField(max_digits=10, decimal_places=2, null=True, editable=False, help_text="Tax applied in Ksh")
    qty = models.IntegerField(default=0, editable=False, null=True,  help_text="Quantity of items")

    def __str__(self):
        return f"Payment {self.payment.payment_id} for Order {self.order.id} (Total: {self.amount_paid} Ksh)"

    class Meta:
        verbose_name_plural = "Payment Orders"
