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
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=125, null=False, blank=False)

    description = models.TextField(blank=True)
    sales_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=True, help_text="Percentage discount")
    qty = models.IntegerField(default=0, null=False, help_text="Available stock quantity")
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, help_text="Buying price")
    currency = models.CharField(max_length=3, default="Ksh")
    unit = models.CharField(max_length=50, null=True, blank=True, default="piece", help_text="Unit of measurement (e.g., piece, plate, pair)")
    tax_category = models.ForeignKey(TaxCategory, on_delete=models.RESTRICT, related_name="products")
    slug = models.SlugField(max_length=125, unique=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    volume = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Volume in liters (e.g., 1.0 L)")
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Weight in grams (e.g., 500g)")

    def __str__(self):
        currency_display = self.currency if self.currency else "Unknown Currency"
        return f"{self.name} - {currency_display} {self.price:,.2f}"




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
