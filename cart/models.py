from django.db import models
from inventory.models import Product
from django.utils.text import slugify
from django.utils import timezone
from inventory.models import CounterStock, Product

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
    quantity = models.DecimalField(max_digits=10, decimal_places=2, help_text="Quantity of product used per order")

    def _str_(self):
        return f"{self.quantity} {self.product.unit} of {self.product.name} for {self.menu_item.name}"

    def deduct_stock(self, order_quantity):
        """Deducts stock from CounterStock when an order is placed."""
        counter_stock = CounterStock.objects.filter(product=self.product).first()

        if counter_stock:
            required_stock = self.quantity * order_quantity

            # Check if there's enough stock
            if counter_stock.current_stock >= required_stock:
                counter_stock.current_stock -= required_stock
                counter_stock.save()
            else:
                # Handle insufficient stock case (optional: raise error or log message)
                raise ValueError(f"Not enough stock for {self.product.name}. Only {counter_stock.current_stock} available.")
        else:
            # Handle case when there's no stock in the counter (optional: create counter stock entry)
            raise ValueError(f"No stock entry for {self.product.name} in the counter.")


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

    def save(self, *args, **kwargs):
        """
        When an order is marked as 'paid', create OrderItems and update stock.
        """
        if self.pk:  # Ensure this is an update, not a new order
            previous_order = Order.objects.filter(pk=self.pk).first()
            if previous_order and previous_order.status != "paid" and self.status == "paid":
                # Order has just been marked as paid → Create OrderItem entries
                self.create_order_items()
                self.update_sold_stock()

        super().save(*args, **kwargs)

    def create_order_items(self):
        """
        Creates OrderItem records from session-based cart.
        """
        from django.contrib.sessions.models import Session
        session = Session.objects.filter(expire_date__gte=timezone.now()).first()

        if session:
            cart = session.get_decoded().get("cart", [])  # Retrieve cart from session
            for item in cart:
                menu_item = MenuItem.objects.get(id=item["menu_item_id"])
                OrderItem.objects.create(
                    order=self,
                    menu_item=menu_item,
                    quantity=item["quantity"]
                )

            session.get_decoded()["cart"] = []  # Clear the cart after checkout
            session.save()

    def update_sold_stock(self):
        """
        Deduct sold items from counter stock when an order is paid.
        """
        for order_item in self.order_items.all():
            product_name = order_item.menu_item.name  # Match CounterStock by name
            counter_stock = CounterStock.objects.filter(product__name=product_name).first()


            if counter_stock:
                counter_stock.qty = max(counter_stock.qty - order_item.quantity, 0)
                counter_stock.save()





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

    def deduct_stock(self):
        """Deduct stock from CounterStock when an order is placed."""
        menu_products = MenuItemProduct.objects.filter(menu_item=self.menu_item)

        for menu_product in menu_products:
            counter_stock = CounterStock.objects.filter(product=menu_product.product).first()
            if counter_stock:
                required_quantity = menu_product.quantity * self.quantity
                if counter_stock.current_stock >= required_quantity:
                    counter_stock.current_stock -= required_quantity
                    counter_stock.save()
                else:
                    raise ValueError(f"Not enough stock for {menu_product.product.name}")




