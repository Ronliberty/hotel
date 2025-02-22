import json
from django.views.generic import DetailView,  CreateView, DetailView, TemplateView
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import PaymentOrder, Payment
from cart.models import Order, OrderItem
from .forms import PaymentForm
import pytz
from django.db.models import Sum
from django.utils.timezone import now
from django.utils import timezone
import uuid
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rooms.models import RoomPayment
class PaymentOrderReceiptView(DetailView):
    """
    CBV to generate and display a receipt for a PaymentOrder.
    """
    model = PaymentOrder
    template_name = "payment/receipt.html"
    context_object_name = "payment_order"

    def get_context_data(self, **kwargs):
        # Fetch additional context data for the receipt
        context = super().get_context_data(**kwargs)
        payment_order = self.object
        context.update({
            "order": payment_order.order,
            "payment": payment_order.payment,
            "user": payment_order.payment.user,
            "date": payment_order.payment.date_time,
        })
        return context
    def test_func(self):
        return self.request.user.groups.filter(name__in=['manager', 'cashier']).exists()

class TotalPaymentsView(LoginRequiredMixin, TemplateView):
    """
    Class-based view to calculate and display total payments for rooms and orders.
    """
    template_name = "payments/total_payments.html"  # Update with your actual template path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total_room_payments = RoomPayment.objects.aggregate(total=Sum('amount'))['total'] or 0.00
        total_order_payments = Payment.objects.aggregate(total=Sum('amount'))['total'] or 0.00

        context.update({
            "total_room_payments": float(total_room_payments),
            "total_order_payments": float(total_order_payments),
            "total_received": float(total_room_payments + total_order_payments),
            "currency": "Ksh",
            "date": now().strftime("%Y-%m-%d %H:%M:%S"),
        })

        return context
class PrintReceiptView(DetailView):
    model = Payment
    template_name = "payment/print_receipt.html"
    context_object_name = "payment"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = OrderItem.objects.filter(order=self.object.order)
        return context

class PaymentDetailView(LoginRequiredMixin, DetailView):
    model = Payment
    template_name = 'payment/payment_detail.html'  # Replace with your template path
    context_object_name = 'payment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        payment = self.object
        payment_order = payment.payment_orders.first() # Example: Get associated PaymentOrder
        context['balance'] = payment.total_payment - payment.amount_paid
        if payment_order:
            context['payment_order'] = payment_order
        else:
            context['payment_order'] = None  # If no related PaymentOrder, set to None

        return context
    def test_func(self):
        return self.request.user.groups.filter(name__in=['manager', 'cashier']).exists()


class PaymentCreateView(LoginRequiredMixin, CreateView):
    model = Payment
    template_name = 'payment/payment_form.html'  # Replace with your template path
    form_class = PaymentForm
    exclude = ['payment_dt']

    def get_form_kwargs(self):
        """Pass the order to the form."""
        kwargs = super().get_form_kwargs()
        order_id = self.kwargs.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        kwargs['order'] = order
        return kwargs

    def form_valid(self, form):
        order = form.instance.order  # Ensure correct order retrieval

        # Ensure order is pending or partially paid
        if order.status not in ['pending', 'partially_paid']:
            raise ValidationError("Only 'pending' or 'partially_paid' orders can be completed with a payment.")

        # Assign user, order, and generate unique payment_id
        form.instance.user = self.request.user
        form.instance.payment_id = str(uuid.uuid4())

        # Set timezone to Kenya
        kenya_tz = pytz.timezone('Africa/Nairobi')
        form.instance.payment_dt = timezone.now().astimezone(kenya_tz)

        # Save the payment instance but do not commit yet
        payment = form.save(commit=False)

        # Calculate the total paid amount
        total_paid = order.payments.aggregate(total=models.Sum('amount_paid'))['total'] or 0
        total_paid += payment.amount_paid

        # Calculate the balance correctly (avoid negative values)
        balance = max(order.total_payment - total_paid, 0)
        payment.balance = balance  # Assign the corrected balance
        payment.save()

        # Update order status
        if balance == 0:
            order.status = 'paid'
        else:
            order.status = 'partially_paid'
        order.save()

        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the payment detail view
        return reverse('payment:payment-detail', kwargs={'pk': self.object.id})
    def test_func(self):
        return self.request.user.groups.filter(name__in=['manager', 'cashier']).exists()






# MPESA API Credentials


# Function to get Mpesa Access Token
def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=HTTPBasicAuth(MPESA_CONSUMER_KEY, MPESA_CONSUMER_SECRET))
    data = response.json()
    return data.get("access_token")

# Register M-Pesa Confirmation URL
def register_mpesa_urls():
    access_token = get_access_token()
    url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "ShortCode": MPESA_SHORTCODE,
        "ResponseType": "Completed",
        "ConfirmationURL": CONFIRMATION_URL,
        "ValidationURL": VALIDATION_URL
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# M-Pesa Payment Confirmation Endpoint
@csrf_exempt
def mpesa_confirmation(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))

            transaction_id = data.get("TransID")
            amount = float(data.get("TransAmount", 0))
            phone_number = data.get("MSISDN")
            bill_ref = data.get("BillRefNumber")  # Maps to Order ID

            # Ensure the order exists
            order = get_object_or_404(Order, id=bill_ref)

            # Prevent duplicate payments
            if Payment.objects.filter(payment_id=transaction_id).exists():
                return JsonResponse({"ResultCode": 1, "ResultDesc": "Duplicate transaction"})

            # Set timezone to Kenya
            kenya_tz = pytz.timezone("Africa/Nairobi")
            payment_dt = timezone.now().astimezone(kenya_tz)

            # Calculate new balance
            new_balance = max(order.total_price - amount, 0)

            # Create a payment record
            Payment.objects.create(
                order=order,
                payment_id=transaction_id,
                total_payment=order.total_price,
                amount_paid=amount,
                balance=new_balance,
                payment_type="MOBILE",
                user=order.user if order.user else None,
                payment_dt=payment_dt
            )

            # Update order status
            order.status = "paid" if new_balance == 0 else "partially_paid"
            order.save()

            return JsonResponse({"ResultCode": 0, "ResultDesc": "Payment processed successfully"})

        except json.JSONDecodeError:
            return JsonResponse({"ResultCode": 1, "ResultDesc": "Invalid JSON format"})
        except Order.DoesNotExist:
            return JsonResponse({"ResultCode": 1, "ResultDesc": "Order not found"})
        except Exception as e:
            return JsonResponse({"ResultCode": 1, "ResultDesc": f"Error: {str(e)}"})

    return JsonResponse({"ResultCode": 1, "ResultDesc": "Invalid request method"})

