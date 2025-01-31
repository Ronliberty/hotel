from django.db import models
from inventory.models import Product
from django.utils.text import slugify
from django.utils import timezone

class MenuCategory(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)



class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='menu_items')
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="Ksh")
    volume = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,default=1, help_text="Volume in liters (e.g., 1.0 L)")
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=1, help_text="Weight in grams (e.g., 500g)")
    unit = models.CharField(max_length=50, null=True, blank=True, default="piece", help_text="Unit of measurement (e.g., piece, plate, pair)")
    is_available = models.BooleanField(default=True)

    def __str__(self):
        currency_display = self.currency if self.currency else "Unknown Currency"
        return f"{self.name} - {currency_display} {self.price:,.2f}"

    def calculate_cost(self):
        """
        Calculate the total cost of raw materials used for this menu item.
        """
        total_cost = sum(
            mip.quantity * mip.product.cost_per_unit for mip in self.menu_item_products.all()
        )
        return total_cost



class MenuItemProduct(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='menu_item_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='menu_item_products')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, help_text="Quantity of product used")

    def __str__(self):
        return f"{self.quantity} {self.product.unit} of {self.product.name} for {self.menu_item.name}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('served', 'Served'),
        ('paid', 'Paid'),
    ]

    table_number = models.IntegerField(blank=True, null=True, help_text="Table number, leave blank for takeaway")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    customer_name = models.CharField(max_length=100, null=True, blank=True, default="guest")
    deleted_at = models.DateTimeField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    def __str__(self):
        return f"Order {self.id} - Table {self.table_number}"

    def delete(self, using=None, keep_parents=False):
        """
        Soft delete the order by setting the `deleted_at` field instead of deleting it.
        Only allows soft delete for orders that are in the 'pending' status.
        """
        if self.status == 'pending':
            self.deleted_at = timezone.now()
            self.status = 'deleted'
            self.save()
        else:
            super().delete(using=using, keep_parents=keep_parents)





class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    special_requests = models.TextField(blank=True, null=True)
    served_by = models.CharField(max_length=100, null=True, blank=True, help_text="Staff or cashier handling the transaction")

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} (Order {self.order.id})"

    @property
    def total_price(self):
        return self.quantity * self.menu_item.price




