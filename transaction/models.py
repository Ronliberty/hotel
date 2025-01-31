from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db import models
from django.db.models import F
from inventory.models import Product



class transaction(models.Model):
    date_time       = models.DateTimeField(auto_now_add=True)
    transaction_dt  = models.DateTimeField(editable=False, null=False, blank=False)
    user            = models.ForeignKey(
                        settings.AUTH_USER_MODEL,
                        on_delete=models.RESTRICT,
                        null=False, blank=False, editable=False
                     )
    transaction_id  = models.CharField(unique=True, max_length=50, editable=False, null=False)
    payment_id = models.CharField(unique=True, max_length=50, editable=False, null=False)
    total_sale      = models.DecimalField(max_digits=7, decimal_places=2, null=False, editable=False)
    sub_total       = models.DecimalField(max_digits=7, decimal_places=2, null=False, editable=False)
    tax_total       = models.DecimalField(max_digits=7, decimal_places=2, null=True, editable=False)
    deposit_total   = models.DecimalField(max_digits=7, decimal_places=2, null=True, editable=False)
    payment_type    = models.CharField(
                        choices=[('CASH', 'CASH'), ('DEBIT/CREDIT', 'DEBIT/CREDIT'), ('EBT', 'EBT')],
                        max_length=32, null=False, editable=False
                     )
    receipt         = models.TextField(blank=False, null=False, editable=False)

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    served_by       = models.CharField(max_length=100, null=True, blank=True, help_text="Staff or cashier handling the transaction")

    def __str__(self) -> str:
        return self.transaction_id

    def save(self, *args, **kwargs):
        # Localize the transaction datetime to ensure timezone correctness
        self.transaction_dt = timezone.localtime(self.transaction_dt)
        super().save(*args, **kwargs)

        # Parse and process products for productTransaction creation
        for product_item in eval(self.products):
            try:
                item = Product.objects.get(name=product_item['name'])
            except Product.DoesNotExist:
                raise ValueError(f"Product with name {product_item['name']} does not exist.")

            productTransaction.objects.create(
                transaction=self,
                transaction_id_num=self.transaction_id,
                transaction_date_time=self.transaction_dt,
                name=product_item['name'],
                sub_category=item.sub_category.name,  # Replaced department with sub_category
                sales_price=product_item['price'],
                qty=product_item['quantity'],
                cost_price=item.cost_price,
                tax_category=item.tax_category.tax_category,
                tax_percentage=item.tax_category.tax_percentage,
                tax_amount=product_item['tax_value'],
                deposit_category=item.deposit_category.deposit_category,
                deposit=item.deposit_category.deposit_value,
                deposit_amount=product_item['deposit_value'],
                payment_type=self.payment_type
            )
        return self

    class Meta:
        verbose_name_plural = "Transactions"



class productTransaction(models.Model):
    transaction             = models.ForeignKey(
                                "transaction",
                                on_delete=models.RESTRICT,
                                null=False, blank=False, editable=False
                             )
    transaction_id_num      = models.CharField(max_length=50, editable=False, null=False)
    transaction_date_time   = models.DateTimeField(editable=False, null=False, blank=False)
    name                    = models.CharField(max_length=125, editable=False, blank=False, null=False)
    sub_category            = models.CharField(max_length=125, editable=False, blank=False, null=True)  # Replacing department
    sales_price             = models.DecimalField(max_digits=7, decimal_places=2, editable=False, null=False, blank=False)
    qty                     = models.IntegerField(default=0, editable=False, null=True)
    cost_price              = models.DecimalField(max_digits=7, decimal_places=2, editable=False, default=0, null=True)
    tax_category            = models.CharField(max_length=125, editable=False, blank=False, null=False)
    tax_percentage          = models.DecimalField(max_digits=6, decimal_places=3, null=False, blank=False)
    tax_amount              = models.DecimalField(max_digits=7, decimal_places=2, editable=False, default=0, null=True)
    deposit_category        = models.CharField(max_length=125, editable=False, blank=False, null=False)
    deposit                 = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False)
    deposit_amount          = models.DecimalField(max_digits=7, decimal_places=2, editable=False, default=0, null=True)
    payment_type            = models.CharField(max_length=32, null=False, editable=False)

    def save(self, *args, **kwargs):
        # Update the quantity of the associated product
        if Product.objects.filter(name=self.name).exists():
            Product.objects.filter(name=self.name).update(qty=F('qty') - self.qty)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.transaction_id_num}_{self.name}"

    class Meta:
        verbose_name_plural = "Product Transactions"


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[('cash', 'Cash'), ('card', 'Card')])
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order {self.order.id} - {self.payment_method}"
