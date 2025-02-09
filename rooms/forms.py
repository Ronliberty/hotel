from django import forms
from .models import Booking, RoomPayment, Room, Feature


class RoomAvailabilityForm(forms.Form):
    check_in_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    check_out_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))



class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [ 'room', 'customer_name', 'customer_phone', 'check_in_date', 'check_out_date', 'guests']

        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'room': 'Select Room',
            'customer_name': 'Full Name',
            'customer_phone': 'Phone Number',
            'check_in_date': 'Check-in Date',
            'check_out_date': 'Check-out Date',
            'guests': 'Number of Guests',
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')
        room = cleaned_data.get('room')
        guests = cleaned_data.get('guests')

        if check_in_date and check_out_date and check_out_date <= check_in_date:
            self.add_error('check_out_date', "Check-out date must be after the check-in date.")

        if room and guests and guests > room.capacity:
            self.add_error('guests', f"The number of guests exceeds the room's capacity of {room.capacity}.")

        if room and check_in_date and check_out_date and not room.is_available_for_dates(check_in_date, check_out_date):
            raise forms.ValidationError("The selected room is not available for the chosen dates.")

        return cleaned_data


class RoomPaymentForm(forms.ModelForm):
    class Meta:
        model = RoomPayment
        fields = ['payment_method', 'amount']  # Include amount here
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'})  # Add widget for amount
        }
        labels = {
            'payment_method': 'Payment Method',
            'amount': 'Amount',
        }

    def __init__(self, *args, **kwargs):
        # Get the booking object from kwargs
        booking = kwargs.pop('booking', None)
        super(RoomPaymentForm, self).__init__(*args, **kwargs)

        if booking:
            # Set the initial value of 'amount' field to the booking's total price
            self.fields['amount'].initial = booking.total_price  # Set the initial value for 'amount'


class RoomCreateForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'room_type', 'capacity', 'price_per_night', 'description', 'features', 'image'] # Include amount here
        widgets = {
            'room_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter room number'}),
            'room_type': forms.Select(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'price_per_night': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter room description'}),
            'features': forms.CheckboxSelectMultiple(),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class RoomFeatureForm(forms.ModelForm):
    class Meta:
        model = Feature
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter feature name'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Enter feature description', 'rows': 3}),
        }