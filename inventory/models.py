import uuid
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]

class MainCategory(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)








class SubCategory(models.Model):
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    def __str__(self):
        return f"{self.main_category.name} -> {self.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)




class TaxCategory(models.Model):
    tax_category = models.CharField(max_length=32, unique=True, null=False, blank=False)
    tax_desc = models.TextField(blank=True)
    tax_percentage = models.DecimalField(max_digits=6, decimal_places=3, validators=PERCENTAGE_VALIDATOR, null=False,
                                         blank=False)

    def __str__(self):
        return self.tax_category

    class Meta:
        verbose_name_plural = "Tax Information"





class Product(models.Model):
    CHOICES = [
        ('store', 'Store'),
        ('counter', 'Counter'),
        ('kitchen', 'Kitchen'),
        ]
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=125, null=False, blank=False)
    supplier = models.CharField(max_length=125, null=False, blank=False, default='anonymous')  # Manually entered
    bought_at = models.DateTimeField(null=True, blank=True)  # Manually entered date
    invoice_number = models.CharField(max_length=50, null=False, blank=False, default="INV-0001")

    description = models.TextField(blank=True)
    sales_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=True, help_text="Percentage discount")
    qty = models.IntegerField(default=0, null=False, help_text="Available stock quantity")
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, help_text="Buying price")
    currency = models.CharField(max_length=3, default="Ksh")
    unit = models.CharField(max_length=50, null=True, blank=True, default="piece", help_text="Unit of measurement (e.g., piece, plate, pair)")
    tax_category = models.ForeignKey(TaxCategory, on_delete=models.RESTRICT, related_name="products")
    slug = models.SlugField(max_length=125, unique=True, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    volume = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Volume in liters (e.g., 1.0 L)")
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Weight in grams (e.g., 500g)")



    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Automatically generate a slug from names
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name  # Return only the name to avoid issues in queries






    def get_final_price(self):
        """
        Calculate the final price after discount and tax.
        """
        discount_price = self.sales_price - (self.sales_price * self.discount / 100)
        tax_amount = discount_price * self.tax_category.tax_percentage / 100
        return discount_price + tax_amount

    def clean(self):
        if not self.unit and not self.volume and not self.weight:
            raise ValidationError("You must specify a unit, volume, or weight for the product.")

    # def save(self, *args, **kwargs):
        # Generate code if not already set
        # if not self.code:
        #     self.code = f"P-{uuid.uuid4().hex[:8].upper()}"  # Unique 8-character alphanumeric code
        # # Generate slug
        # if not self.slug:
        #     self.slug = slugify(self.name)
        # super().save(*args, **kwargs)


class CounterStock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="counter_stock")
    qty = models.PositiveIntegerField(default=0, help_text="Stock at the counter")

    moved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.qty} {self.product.unit} at Counter"

    def adjust_stock(self, quantity, movement_type='add'):
        """
        Adjust stock at the counter based on the movement type (add/remove).
        :param quantity: Quantity to add or subtract from the counter stock.
        :param movement_type: Type of movement ('add' or 'remove').
        """
        if movement_type == 'add':
            self.qty += quantity
        elif movement_type == 'remove':
            if self.qty >= quantity:
                self.qty -= quantity
            else:
                raise ValueError("Not enough stock to remove.")
        self.save()


class KitchenStock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="kitchen_stock")
    qty = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Stock in kitchen")
    moved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.qty} {self.product.unit} in Kitchen"



class StockMovement(models.Model):
    STORE_CHOICES = [
        ("store", "Store"),
        ("counter", "Counter"),
        ("kitchen", "Kitchen"),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stock_movements")
    quantity = models.IntegerField()
    source = models.CharField(max_length=10, choices=STORE_CHOICES)
    destination = models.CharField(max_length=10, choices=STORE_CHOICES)
    moved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} {self.product.name} moved from {self.source} to {self.destination} on {self.timestamp}"



class SalesInvoice(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="sales_invoices")
    supplier = models.CharField(max_length=125, null=False, blank=False, default='anonymous')
    bought_at = models.DateTimeField(null=True, blank=True)
    invoice_number = models.CharField(max_length=50, unique=True, null=False, blank=False, default="INV-0001")
    qty_sold = models.PositiveIntegerField(null=False, blank=False, help_text="Quantity sold")
    sales_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, help_text="Selling price per unit")
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=True, help_text="Discount percentage")
    tax_category = models.ForeignKey('TaxCategory', on_delete=models.RESTRICT, related_name="sales_invoices")
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, help_text="Total tax applied")
    currency = models.CharField(max_length=3, default="Ksh", choices=[("Ksh", "Kenyan Shilling")])
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, help_text="Final amount after tax and discount")
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="issued_invoices")

    def save(self, *args, **kwargs):
        # Calculate the total amount dynamically before saving
        discount_value = (self.sales_price * self.qty_sold) * (self.discount / 100)
        taxable_amount = (self.sales_price * self.qty_sold) - discount_value
        self.total_amount = taxable_amount + self.tax_amount  # Adding tax amount to final price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.product.name}"