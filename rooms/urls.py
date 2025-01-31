from django.urls import path
from .views import ( RoomListView, FeatureListView, FeatureCreateView, FeatureDetailView, FeatureUpdateView, FeatureDeleteView, RoomCreateView, RoomDeleteView, RoomDetailView, PaymentSummaryView, RoomsSummaryView, CheckoutListView, CheckoutDetailView,
RoomAvailabilityView, RoomUpdateView, BookingListView, BookingCreateView, BookingDetailView, BookingUpdateView, BookingDeleteView, RoomPaymentFormView, CancelBookingView, PaidPaymentsListView, PaymentDetailView, RoomServiceListView
                 )
app_name = 'rooms'

urlpatterns = [
    #manager
    path('features/', FeatureListView.as_view(), name='feature-list'),
    path('features/add/', FeatureCreateView.as_view(), name='feature-add'),
    path('features/<int:pk>/', FeatureDetailView.as_view(), name='feature-detail'),
    path('features/<int:pk>/edit/', FeatureUpdateView.as_view(), name='feature-edit'),
    path('features/<int:pk>/delete/', FeatureDeleteView.as_view(), name='feature-delete'),

    #manager
    path('rooms/', RoomListView.as_view(), name='rooms-list'),
    path("rooms/service/", RoomServiceListView.as_view(), name="room_service"),

    path('rooms/add/', RoomCreateView.as_view(), name='room-add'),
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
    path('rooms/<int:pk>/edit/', RoomUpdateView.as_view(), name='room-edit'),
    path('rooms/<int:pk>/delete/', RoomDeleteView.as_view(), name='room-delete'),
    path('rooms/<int:pk>/availability/', RoomAvailabilityView.as_view(), name='room-availability'),

    #room Attendant
    path('bookings/', BookingListView.as_view(), name='booking-list'),
    path('bookings/add/', BookingCreateView.as_view(), name='booking-add'),
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
    path('bookings/<int:pk>/edit/', BookingUpdateView.as_view(), name='booking-edit'),
    path('bookings/<int:pk>/delete/', BookingDeleteView.as_view(), name='booking-delete'),
    path('booking/<int:pk>/cancel/', CancelBookingView.as_view(), name='cancel-booking'),
    path('checkouts/', CheckoutListView.as_view(), name='checkout_list'),
    path("checkout/<int:pk>/", CheckoutDetailView.as_view(), name="checkout_detail"),


    path('booking/<int:pk>/payment/', RoomPaymentFormView.as_view(), name='add-payment'),
    path('payments/', PaidPaymentsListView.as_view(), name='paid_payments_list'),
    path('payments/<int:pk>/', PaymentDetailView.as_view(), name='payment_detail'),
    path('payments/summary/', PaymentSummaryView.as_view(), name='payment_summary'),
    path('summary/', RoomsSummaryView.as_view(), name='rooms-summary'),

]