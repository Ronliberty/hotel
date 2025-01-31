from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, View
from .models import MenuCategory, MenuItemProduct, MenuItem, Order, OrderItem
from payment.models import Payment
from django.db.models import Sum

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from decimal import Decimal
import re
from django.http import HttpResponseForbidden
from django.utils.timezone import now

class MenuCategoryCreateView(CreateView):
    model = MenuCategory
    fields = ['name', 'description']
    template_name = 'cart/menu_category_form.html'
    success_url = reverse_lazy('cart:menu_category_list')

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()


class MenuCategoryListView(ListView):
    model = MenuCategory
    template_name = 'cart/menu_category_list.html'
    context_object_name = 'categories'

    def test_func(self):
        return self.request.user.groups.filter(name__in=['manager', 'storekeeper', 'cashier']).exists()


class MenuCategoryDetailView(DetailView):
    model = MenuCategory
    template_name = 'cart/menu_category_detail.html'
    context_object_name = 'category'

    def test_func(self):
        return self.request.user.groups.filter(name__in=['manager', 'storekeeper', 'cashier']).exists()


class MenuCategoryUpdateView(UpdateView):
    model = MenuCategory
    fields = ['name', 'description']
    template_name = 'cart/menu_category_form.html'
    success_url = reverse_lazy('cart:menu_category_list')
    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()



class MenuCategoryDeleteView(DeleteView):
    model = MenuCategory
    template_name = 'cart/menu_category_confirm_delete.html'
    success_url = reverse_lazy('cart:menu_category_list')
    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()



class MenuItemProductCreateView(CreateView):
    model = MenuItemProduct
    fields = ['menu_item', 'product', 'quantity']
    template_name = 'cart/menu_item_product_form.html'
    success_url = reverse_lazy('cart:menu_item_product_list')
    def test_func(self):
        return self.request.user.groups.filter(name__in=['manager', 'storekeeper']).exists()


class MenuItemProductListView(ListView):
    model = MenuItemProduct
    template_name = 'cart/menu_item_product_list.html'
    context_object_name = 'menu_item_products'

    def test_func(self):
        return self.request.user.groups.filter(name__in=['manager', 'storekeeper']).exists()


class MenuItemProductDetailView(DetailView):
    model = MenuItemProduct
    template_name = 'cart/menu_item_product_detail.html'
    context_object_name = 'menu_item_product'

    def test_func(self):
        return self.request.user.groups.filter(name__in=['manager', 'storekeeper']).exists()


class MenuItemProductUpdateView(UpdateView):
    model = MenuItemProduct
    fields = ['menu_item', 'product', 'quantity']
    template_name = 'cart/menu_item_product_form.html'
    success_url = reverse_lazy('cart:menu_item_product_list')
    def test_func(self):
        return self.request.user.groups.filter(name__in=['manager', 'storekeeper']).exists()
    def test_func(self):
        return self.request.user.groups.filter(name__in=['manager', 'storekeeper']).exists()

class MenuItemProductDeleteView(DeleteView):
    model = MenuItemProduct
    template_name = 'cart/menu_item_product_confirm_delete.html'
    success_url = reverse_lazy('cart:menu_item_product_list')
    def test_func(self):
        return self.request.user.groups.filter(name__in=['manager', 'storekeeper']).exists()
    def test_func(self):
        return self.request.user.groups.filter(name__in=['manager', 'storekeeper']).exists()


class MenuItemListView(ListView):
    model = MenuItem
    template_name = "cart/menuitem_list.html"
    context_object_name = "menu_items"
    paginate_by = 10

    def test_func(self):
        return self.request.user.groups.filter(name__in=[ 'storekeeper', 'cashier']).exists()



class MenuManagerListView(ListView):
    model = MenuItem
    template_name = "cart/menu_list.html"
    context_object_name = "menu_items"


    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()


# DetailView
class MenuItemDetailView(DetailView):
    model = MenuItem
    template_name = "cart/menuitem_detail.html"
    context_object_name = "menu_item"


# CreateView
class MenuItemCreateView(CreateView):
    model = MenuItem
    template_name = "cart/menuitem_form.html"
    fields = ['name', 'category', 'description', 'price', 'is_available', 'currency', 'volume', 'weight', 'unit']
    success_url = reverse_lazy('cart:list_menu')
    def test_func(self):
        return self.request.user.groups.filter(name__in=['manager', 'storekeeper']).exists()


# UpdateView
class MenuItemUpdateView(UpdateView):
    model = MenuItem
    template_name = "cart/menuitem_form.html"
    fields = ['name', 'category', 'description', 'price', 'is_available']
    success_url = reverse_lazy('cart:menuitem-list')
    def test_func(self):
        return self.request.user.groups.filter(name__in=['manager', 'storekeeper']).exists()


# DeleteView
class MenuItemDeleteView(DeleteView):
    model = MenuItem
    template_name = "cart/menuitem_confirm_delete.html"
    success_url = reverse_lazy('cart:list_menu')
    def test_func(self):
        return self.request.user.groups.filter(name__in=['manager', 'storekeeper']).exists()


class CartView(View):
    """
    Display the current items in the cart.
    """
    template_name = "cart/cart.html"

    def get(self, request):
        cart = request.session.get("cart", [])
        total_price = sum(float(item["price"].replace("Ksh ", "")) * item["quantity"] for item in cart)
        return render(request, self.template_name, {"cart": cart, "total_price": total_price})
    def test_func(self):
        return self.request.user.groups.filter(name='cashier').exists()


class AddToCartView(View):
    """
    Add an item to the cart stored in the session.
    """

    def post(self, request, menu_item_id):
        menu_item = get_object_or_404(MenuItem, id=menu_item_id)
        cart = request.session.get("cart", [])

        # Check if there's an existing pending order, if none, create a new one
        order = Order.objects.filter(status='pending').first()  # Find the first pending order

        if not order:  # If there's no pending order, create a new one
            order = Order.objects.create(status='pending')

        # Check if item is already in cart
        for item in cart:
            if item["menu_item_id"] == menu_item.id:
                item["quantity"] += 1
                break
        else:
            # Add new item to cart
            cart.append({
                "menu_item_id": menu_item.id,
                "name": menu_item.name,
                "price": f"Ksh {float(menu_item.price):,.2f}",
                "quantity": 1,
            })

        request.session["cart"] = cart
        return redirect("cart:cart")

    def test_func(self):
        return self.request.user.groups.filter(name='cashier').exists()


class RemoveFromCartView(View):
    """
    Remove an item from the cart stored in the session.
    """
    def post(self, request, menu_item_id):
        cart = request.session.get("cart", [])
        cart = [item for item in cart if item["menu_item_id"] != menu_item_id]
        request.session["cart"] = cart
        return redirect("cart:cart")
    def test_func(self):
        return self.request.user.groups.filter(name='cashier').exists()


class UpdateCartItemView(View):
    """
    Update the quantity of an item in the cart.
    """
    def post(self, request, menu_item_id):
        new_quantity = int(request.POST.get("quantity", 1))
        cart = request.session.get("cart", [])

        for item in cart:
            if item["menu_item_id"] == menu_item_id:
                item["quantity"] = new_quantity
                break

        request.session["cart"] = cart
        return redirect("cart:cart")
    def test_func(self):
        return self.request.user.groups.filter(name='cashier').exists()


class ConfirmOrderView(View):
    """
    Confirm the order and save it to the database.
    """
    def post(self, request):
        cart = request.session.get("cart", [])
        if not cart:
            return redirect("cart:cart")

        # Ensure price and quantity are treated as numbers
        total_price = sum(float(item['price'].replace('Ksh ', '').strip()) * int(item['quantity']) for item in cart)

        # Create an Order instance with the calculated total price
        order = Order.objects.create(total_price=total_price)

        # Add items to the order
        for item in cart:
            menu_item = get_object_or_404(MenuItem, id=item["menu_item_id"])
            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=item["quantity"],
            )

        # Clear the cart from the session
        request.session["cart"] = []

        return redirect("cart:order-detail", pk=order.id)

    def test_func(self):
        return self.request.user.groups.filter(name='cashier').exists()


class CancelOrderView(View):
    """
    Cancel the current cart by clearing the session.
    """
    def post(self, request):
        request.session["cart"] = []
        return redirect("cart:cart")
    def test_func(self):
        return self.request.user.groups.filter(name='cashier').exists()


def search_menu_item(request):
    from decimal import Decimal
    import re

    query = request.GET.get('query', '')
    menu_items = MenuItem.objects.filter(name__icontains=query) if query else []
    cart = request.session.get("cart", [])

    # Helper function to parse and clean the price string
    def parse_price(price_str):
        try:
            # Use regex to remove non-numeric characters except '.'
            numeric_part = re.sub(r'[^\d.]', '', price_str)
            return Decimal(numeric_part)
        except (ValueError, Decimal.InvalidOperation):
            return Decimal(0)  # Default to 0 if parsing fails

    # Calculate total price
    total_price = sum(parse_price(item['price']) * item['quantity'] for item in cart)

    return render(request, 'cart/cart.html', {
        'menu_items': menu_items,
        'cart': cart,
        'total_price': total_price
    })



class OrderDetailView(DetailView):
    model = Order
    template_name = 'cart/order_detail.html'  # Replace with your detail template
    context_object_name = 'order'
    def test_func(self):
        return self.request.user.groups.filter(name__in=['manager', 'cashier']).exists()


class PendingOrdersView(ListView):
    """
    View for displaying all pending orders.
    """
    model = Order
    template_name = 'cart/pending_orders.html'  # Replace with your template path
    context_object_name = 'pending_orders'  # The context variable for the list of orders

    def get_queryset(self):
        # Get all orders that are still pending
        return Order.objects.filter(status='pending')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the total price to the context for each order
        for order in context['pending_orders']:
            order.total_price_formatted = order.total_price  # Add formatted price to display
        return context

    def test_func(self):
        return self.request.user.groups.filter(name__in=['manager', 'cashier']).exists()



class CompletedOrdersView(ListView):
    """
    View for displaying all completed orders.
    """
    model = Order
    template_name = 'cart/completed_orders.html'  # Replace with your template path
    context_object_name = 'completed_orders'  # The context variable for the list of completed orders

    def get_queryset(self):
        # Get all orders that are completed (assuming 'paid' is the completed status)
        return Order.objects.filter(status='paid')

    def get_context_data(self, **kwargs):
        # Get the default context data from the superclass
        context = super().get_context_data(**kwargs)

        # Calculate the grand total
        grand_total = sum(order.total_price for order in context['completed_orders'])

        # Add the grand total to the context
        context['grand_total'] = grand_total

        return context

    def test_func(self):
        return self.request.user.groups.filter(name__in=['manager', 'cashier']).exists()

class DailySalesView(ListView):
    """
    View for displaying all completed payments for the current day.
    """
    model = Payment  # Change to Payment model to track actual payments
    template_name = 'cart/daily_sales.html'  # Replace with your template path
    context_object_name = 'daily_sales'  # The context variable for the list of daily payments

    def get_queryset(self):
        """
        Get all payments recorded today.
        """
        today = now().date()  # Get today's date
        return Payment.objects.filter(payment_dt__date=today)  # Filter payments made today

    def get_context_data(self, **kwargs):
        """
        Add total sales amount to the context.
        """
        context = super().get_context_data(**kwargs)

        # Calculate the total amount paid today
        daily_total = Payment.objects.filter(payment_dt__date=now().date()).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0

        # Add daily total to context
        context['daily_total'] = daily_total

        return context

class DeletedOrderListView(ListView):
    model = Order
    template_name = 'cart/deleted_orders_list.html'  # Template to display the deleted orders
    context_object_name = 'deleted_orders'

    def get_queryset(self):
        # Fetch orders that have been soft deleted
        return Order.objects.filter(deleted_at__isnull=False)

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()

class DeletedOrderCashierListView(ListView):
    model = Order
    template_name = 'cart/deleted_orders_cashier.html'  # Template to display the deleted orders
    context_object_name = 'deleted_orders'

    def get_queryset(self):
        # Fetch orders that have been soft deleted
        return Order.objects.filter(deleted_at__isnull=False)

    def test_func(self):
        return self.request.user.groups.filter(name='cashier').exists()


def delete_pending_order(request, pk):
    order = get_object_or_404(Order, pk=pk)

    # Ensure that only pending orders can be deleted
    if order.status != 'pending':
        return HttpResponseForbidden("You can only delete pending orders.")

    # Perform soft delete
    order.delete()  # This triggers the custom delete method that sets 'deleted_at' and status to 'deleted'

    return redirect('cart:pending-orders')




