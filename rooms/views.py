from django.shortcuts import render, get_object_or_404, redirect
from .models import Feature, Room, Booking, RoomPayment
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView, View
from .forms import RoomAvailabilityForm, BookingForm, RoomPaymentForm
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from datetime import date

class FeatureListView(ListView):
    model = Feature
    template_name = 'rooms/feature_list.html'  # Update the path as per your template structure
    context_object_name = 'features'

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()


class FeatureCreateView(CreateView):
    model = Feature
    template_name = 'rooms/feature_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('rooms:feature-list')
    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()


class FeatureDetailView(DetailView):
    model = Feature
    template_name = 'rooms/feature_detail.html'
    context_object_name = 'feature'
    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()


class FeatureUpdateView(UpdateView):
    model = Feature
    template_name = 'rooms/feature_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('rooms:feature-list')
    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()


class FeatureDeleteView(DeleteView):
    model = Feature
    template_name = 'rooms/feature_confirm_delete.html'
    success_url = reverse_lazy('rooms:feature-list')
    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()


class RoomListView(ListView):
    model = Room
    template_name = 'rooms/room_list.html'
    context_object_name = 'rooms'
    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()


class RoomCreateView(CreateView):
    model = Room
    template_name = 'rooms/room_form.html'
    fields = ['room_number', 'room_type', 'capacity', 'price_per_night', 'description', 'features', 'image']
    success_url = reverse_lazy('rooms:rooms-list')
    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()




class RoomDetailView(DetailView):
    model = Room
    template_name = 'rooms/room_detail.html'
    context_object_name = 'room'
    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()


class RoomUpdateView(UpdateView):
    model = Room
    template_name = 'rooms/room_form.html'
    fields = ['room_number', 'room_type', 'capacity', 'price_per_night', 'description', 'features', 'image']
    success_url = reverse_lazy('rooms:rooms-list')
    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()


class RoomDeleteView(DeleteView):
    model = Room
    template_name = 'rooms/room_confirm_delete.html'
    success_url = reverse_lazy('rooms:rooms-list')
    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()


class RoomAvailabilityView(View):
    """Check room availability for given dates."""

    def get(self, request, pk):
        room = Room.objects.get(pk=pk)
        form = RoomAvailabilityForm()
        return render(request, 'rooms/room_availability.html', {'room': room, 'form': form})
    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()

    def post(self, request, pk):
        room = Room.objects.get(pk=pk)
        form = RoomAvailabilityForm(request.POST)
        if form.is_valid():
            check_in = form.cleaned_data['check_in_date']
            check_out = form.cleaned_data['check_out_date']
            is_available = room.is_available_for_dates(check_in, check_out)
            return JsonResponse({'available': is_available})
        return JsonResponse({'error': 'Invalid data'}, status=400)

class RoomServiceListView(ListView):
    model = Room
    template_name = "rooms/room_service.html"
    context_object_name = "rooms"

    def get_queryset(self):
        # Optionally filter rooms if needed
        return Room.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()  # Example availability check for today
        for room in context['rooms']:
            room.is_available = room.is_available_for_dates(today, today)
        return context



class BookingListView(ListView):
    model = Booking
    template_name = 'rooms/booking_list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        """Filter bookings by status."""
        return Booking.objects.all().order_by('-booking_date')

    def get_context_data(self, **kwargs):
        """Separate bookings by their status."""
        context = super().get_context_data(**kwargs)
        context['pending_bookings'] = Booking.objects.filter(status='PENDING').order_by('-booking_date')
        context['confirmed_bookings'] = Booking.objects.filter(status='CONFIRMED').order_by('-booking_date')
        context['cancelled_bookings'] = Booking.objects.filter(status='CANCELLED').order_by('-booking_date')
        return context
    def test_func(self):
        return self.request.user.groups.filter(name='storekeeper').exists()


class BookingCreateView(CreateView):
    model = Booking
    template_name = 'rooms/booking_form.html'
    form_class = BookingForm
    success_url = reverse_lazy('rooms:booking-list')

    def form_valid(self, form):
        try:
            form.instance.total_price = form.instance.calculate_total_price()
            form.instance.full_clean()  # Run validations
            return super().form_valid(form)
        except ValidationError as e:
            form.add_error(None, e.message)
            return self.form_invalid(form)

    def get_initial(self):
        initial = super().get_initial()
        room_id = self.request.GET.get('room_id')  # Get room_id from query parameters

        if room_id:
            room = get_object_or_404(Room, id=room_id)
            initial['room'] = room  # Pre-fill the room field with the selected room

        return initial




    def test_func(self):
            return self.request.user.groups.filter(name='roomkeeper').exists()


class BookingDetailView(DetailView):
    model = Booking
    template_name = 'rooms/booking_detail.html'
    context_object_name = 'booking'
    def test_func(self):
        return self.request.user.groups.filter(name='storekeeper').exists()


class BookingUpdateView(UpdateView):
    model = Booking
    template_name = 'rooms/booking_form.html'
    fields = ['room', 'customer_name', 'customer_phone', 'check_in_date', 'check_out_date', 'guests', 'status']
    success_url = reverse_lazy('rooms:booking-list')

    def form_valid(self, form):
        try:
            form.instance.total_price = form.instance.calculate_total_price()
            form.instance.full_clean()  # Run validations
            return super().form_valid(form)
        except ValidationError as e:
            form.add_error(None, e.message)
            return self.form_invalid(form)

        def test_func(self):
            return self.request.user.groups.filter(name='storekeeper').exists()


class BookingDeleteView(DeleteView):
    model = Booking
    template_name = 'rooms/booking_confirm_delete.html'
    success_url = reverse_lazy('rooms:booking-list')
    def test_func(self):
        return self.request.user.groups.filter(name='storekeeper').exists()

class CancelBookingView(View):
    """Handles booking cancellation."""

    def post(self, request, pk):
        # Fetch the booking object
        booking = get_object_or_404(Booking, pk=pk)

        # Check if the booking is already cancelled or completed
        if booking.status == 'CANCELLED':
            messages.warning(request, "This booking is already cancelled.")
            return redirect(reverse('rooms:booking-list'))
        elif booking.status == 'CONFIRMED':
            messages.warning(request, "You cannot cancel a confirmed booking.")
            return redirect(reverse('rooms:booking-list'))

        # Update the booking status
        booking.status = 'CANCELLED'
        booking.save()

        # Optionally, log cancellation or handle refunds here
        messages.success(request, f"Booking {booking.id} has been successfully cancelled.")
        return redirect(reverse('rooms:booking-list'))
    def test_func(self):
        return self.request.user.groups.filter(name='storekeeper').exists()

# ListView for confirmed bookings (checkouts)
class CheckoutListView(ListView):
    model = Booking
    template_name = "rooms/checkout_list.html"  # Updated template name
    context_object_name = "checkouts"  # Updated variable name for templates

    def get_queryset(self):
        # Filter bookings with status "CONFIRMED"
        return Booking.objects.filter(status="CONFIRMED").order_by("-booking_date")

class CheckoutDetailView(DetailView):
    model = Booking
    template_name = "rooms/checkout_detail.html"  # Updated template name
    context_object_name = "checkout"  # Updated variable name for templates

    def get_queryset(self):
        # Ensure only confirmed bookings are shown
        return Booking.objects.filter(status="CONFIRMED")




class RoomPaymentFormView(CreateView):

    form_class = RoomPaymentForm
    template_name = 'rooms/roompayment_form.html'
    success_url = reverse_lazy('payment-list')

    def get_form_kwargs(self):
        # Get the booking using the URL parameter (booking id)
        booking = get_object_or_404(Booking, pk=self.kwargs['pk'])

        # Pass the booking object to the form to pre-populate the amount
        kwargs = super(RoomPaymentFormView, self).get_form_kwargs()
        kwargs['booking'] = booking
        return kwargs

    def form_valid(self, form):
        booking_id = self.kwargs['pk']
        booking = get_object_or_404(Booking, pk=booking_id)

        # Create the payment
        payment = form.save(commit=False)
        payment.booking = booking
        payment.is_paid = True  # Mark payment as paid
        payment.save()

        # Update booking status if fully paid
        if payment.amount >= booking.total_price:
            booking.status = 'CONFIRMED'
            booking.save()

        return redirect(reverse('rooms:booking-detail', args=[booking.id]))
    def test_func(self):
        return self.request.user.groups.filter(name='storekeeper').exists()


class PaymentDetailView(DetailView):
    model = RoomPayment
    template_name = "rooms/payment_detail.html"  # Create this template
    context_object_name = "payment"


class PaidPaymentsListView(ListView):
    model = RoomPayment
    template_name = "rooms/paid_payments_list.html"  # Create this template
    context_object_name = "payments"

    def get_queryset(self):
        return RoomPayment.objects.filter(is_paid=True).order_by('-payment_date')


class PaymentSummaryView(TemplateView):
    template_name = "rooms/payment_summary.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Total by Day
        context['daily_totals'] = RoomPayment.objects.filter(is_paid=True).extra(
            select={'day': "strftime('%Y-%m-%d', payment_date)"}
        ).values('day').annotate(total_amount=Sum('amount')).order_by('-day')

        # Total by Month
        context['monthly_totals'] = RoomPayment.objects.filter(is_paid=True).extra(
            select={'month': "strftime('%Y-%m', payment_date)"}
        ).values('month').annotate(total_amount=Sum('amount')).order_by('-month')

        # Total by Year
        context['yearly_totals'] = RoomPayment.objects.filter(is_paid=True).extra(
            select={'year': "strftime('%Y', payment_date)"}
        ).values('year').annotate(total_amount=Sum('amount')).order_by('-year')

        # Grand Total
        context['grand_total'] = RoomPayment.objects.filter(is_paid=True).aggregate(
            total_amount=Sum('amount')
        )['total_amount']

        return context


class RoomsSummaryView(TemplateView):
    template_name = "dashboard/super_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pass querysets to the template
        context['features'] = Feature.objects.all()
        context['rooms'] = Room.objects.all()
        context['bookings'] = Booking.objects.all()
        context['payments'] = RoomPayment.objects.all()

        # Add summary data for additional display
        context['total_features'] = context['features'].count()
        context['total_rooms'] = context['rooms'].count()
        context['available_rooms'] = context['rooms'].filter(availability_status='available').count()
        context['occupied_rooms'] = context['rooms'].filter(availability_status='occupied').count()
        context['total_bookings'] = context['bookings'].count()
        context['pending_bookings'] = context['bookings'].filter(status='PENDING').count()
        context['confirmed_bookings'] = context['bookings'].filter(status='CONFIRMED').count()
        context['cancelled_bookings'] = context['bookings'].filter(status='CANCELLED').count()
        context['total_payments'] = context['payments'].filter(is_paid=True).count()
        context['total_revenue'] = context['payments'].filter(is_paid=True).aggregate(
            total_revenue=Sum('amount')
        )['total_revenue'] or 0

        # Daily revenue summary
        context['daily_revenue'] = (
            context['payments']
            .filter(is_paid=True)
            .annotate(day=TruncDate('payment_date'))
            .values('day')
            .annotate(total=Sum('amount'))
            .order_by('-day')[:5]
        )

        return context