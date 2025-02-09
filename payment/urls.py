from django.urls import path
from .views import PaymentOrderReceiptView, TotalPaymentsView,  PaymentCreateView, PaymentDetailView, PrintReceiptView, mpesa_confirmation



app_name = 'payment'
urlpatterns = [
    path('paymentreceipt/<int:pk>/', PaymentOrderReceiptView.as_view(), name='print-receipt'),
    path('print-receipt/<int:pk>/', PrintReceiptView.as_view(), name="print-receipt"),
    path('mpesa/confirmation/', mpesa_confirmation, name='mpesa_confirmation'),


    path('create/<int:order_id>/', PaymentCreateView.as_view(), name='payment-create'),
    path('<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),
    path("payments/total/", TotalPaymentsView.as_view(), name="total-payments"),
]
