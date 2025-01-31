from django.urls import path
from .views import PaymentOrderReceiptView, PaymentCreateView, PaymentDetailView, PrintReceiptView



app_name = 'payment'
urlpatterns = [
    path('paymentreceipt/<int:pk>/', PaymentOrderReceiptView.as_view(), name='print-receipt'),
path('print-receipt/<int:pk>/', PrintReceiptView.as_view(), name="print-receipt"),


    path('create/<int:order_id>/', PaymentCreateView.as_view(), name='payment-create'),
    path('<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),
]
