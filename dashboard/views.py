import pytz
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView
from django.utils import timezone
from django.utils.timezone import now
from cart.models import Order
from inventory.models import MainCategory, SubCategory, Product, TaxCategory
from rooms.models import RoomPayment, Room, Booking
from payment.models import Payment, PaymentOrder
from django.db.models import Count, Sum



class BaseDashboardView(LoginRequiredMixin, TemplateView):
    group_name = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name=self.group_name).exists():
            messages.error(request, "You are not authorized to access this page.")
            return redirect('base:index')
        return super().dispatch(request, *args, **kwargs)

class CashierDashboardView(BaseDashboardView):
    template_name = 'dashboard/cashier_dashboard.html'
    group_name = 'cashier'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the Mombasa time zone (Kenya's time zone)
        mombasa_tz = pytz.timezone('Africa/Nairobi')  # Mombasa is in 'Africa/Nairobi' timezone
        # Get the current time in Mombasa (East Africa Time - UTC+3)
        current_time = timezone.now().astimezone(mombasa_tz)
        context['current_time'] = current_time  # Pass the Mombasa time to the template

        # Check if the logged-in user is in the "cashier" group
        if self.request.user.groups.filter(name=self.group_name).exists():
            context['cashier'] = self.request.user  # Only add cashier data if the user is part of the "cashier" group
        else:
            context['cashier'] = None  # Handle the case where the user is not part of the "cashier" group

        return context



class ManagerDashboardView(BaseDashboardView):
    template_name = 'dashboard/manager_dashboard.html'
    group_name = 'manager'

    def get_context_data(self, **kwargs):
        # Get the default context data from the superclass
        context = super().get_context_data(**kwargs)

        # Calculate today's total sales
        today = now().date()  # Get the current date
        today_sales = Order.objects.filter(status='paid',
                                           created_at__date=today)  # Filter orders that are paid and created today

        daily_total = sum(order.total_price for order in today_sales)  # Calculate the total sales for the day

        # Add the total sales to the context
        context['daily_total'] = daily_total

        return context



class StoreDashboardView(BaseDashboardView):
    template_name = 'dashboard/store_dashboard.html'
    group_name = 'storekeeper'



class RoomsDashboardView(BaseDashboardView):
    template_name = 'dashboard/rooms_dashboard.html'
    group_name = 'roomkeeper'

class SuperDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/super_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        if self.group_name and not request.user.groups.filter(name=self.group_name).exists():
            messages.error(request, "You are not authorized to access this page")
            return redirect('base:index')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add inventory summary data
        context['main_category_count'] = MainCategory.objects.count()
        context['sub_category_count'] = SubCategory.objects.count()
        context['product_count'] = Product.objects.count()
        context['tax_category_count'] = TaxCategory.objects.count()

        # Add additional data as needed
        context['recent_products'] = Product.objects.order_by('-created_at')[:15]  # Last 5 products
        context['recent_categories'] = MainCategory.objects.order_by('-id')[:5]  # Last 5 categories

        context['total_rooms'] = Room.objects.count()
        # context['available_rooms'] = Room.objects.filter(is_available=True).count()
        context['total_bookings'] = Booking.objects.count()
        context['pending_bookings'] = Booking.objects.filter(status='PENDING').count()
        context['confirmed_bookings'] = Booking.objects.filter(status='CONFIRMED').count()
        context['cancelled_bookings'] = Booking.objects.filter(status='CANCELLED').count()
        total_payment_rooms = RoomPayment.objects.aggregate(
            total=Sum('amount')
        )['total'] or 0


        # Payment summary
        context['total_payments'] = RoomPayment.objects.filter(is_paid=True).aggregate(total=Sum('amount'))[
                                        'total'] or 0


        context['payments'] = Payment.objects.all()
        total_payment_payments = Payment.objects.aggregate(
            total=Sum('total_payment')
        )['total'] or 0

        context['recent_payments'] = RoomPayment.objects.filter(is_paid=True).order_by('-payment_date')[:9]

        # Calculate total room payments
        total_payment_rooms = RoomPayment.objects.filter(is_paid=True).aggregate(
            total=Sum('amount')
        )['total'] or 0
        context['total_payment_rooms'] = total_payment_rooms
        combined_total_payment = total_payment_payments + total_payment_rooms
        context['total_payment_payments'] = total_payment_payments
        context['total_payment_rooms'] = total_payment_rooms
        context['combined_total_payment'] = combined_total_payment

        # Add payment orders details to the context
        context['payment_orders'] = PaymentOrder.objects.all()


        return context

