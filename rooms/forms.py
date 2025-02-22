from django import forms
from .models import Booking, RoomPayment, Room, Feature


class RoomAvailabilityForm(forms.Form):
    check_in_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    check_out_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))



class BookingForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    EXECUTIVE_CHOICES = [
        ('Bed & Breakfast', 'Bed & Breakfast'),
        ('Bed Only', 'Bed Only'),
        ('Halfboard', 'Halfboard'),
        ('Fullboard', 'Fullboard'),
    ]

    ID_TYPE_CHOICES = [
        ('National ID', 'National ID'),
        ('Passport', 'Passport'),
        ('Driver\'s License', 'Driver\'s License'),
    ]

    id_type = forms.ChoiceField(choices=ID_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    customer_id = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Government ID'}),
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    executive_choice = forms.ChoiceField(choices=EXECUTIVE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Booking
        fields = ['id_type', 'customer_id', 'customer_name', 'gender', 'customer_phone', 'room', 'check_in_date', 'check_out_date', 'guests', 'executive_choice']

        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Full Name'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
            'room': forms.Select(attrs={'class': 'form-control'}),
            'guests': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
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

        # Ensure check-out date is after check-in date
        if check_in_date and check_out_date and check_out_date <= check_in_date:
            self.add_error('check_out_date', "Check-out date must be after the check-in date.")

        # Ensure number of guests does not exceed room capacity
        if room and guests:
            if guests > room.capacity:
                self.add_error('guests', f"The number of guests exceeds the room's capacity of {room.capacity}.")

        # Ensure room availability for the selected dates
        if room and check_in_date and check_out_date:
            if not room.is_available_for_dates(check_in_date, check_out_date):
                self.add_error(None, "The selected room is not available for the chosen dates.")

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
        fields = [
            'room_number', 'room_type', 'capacity', 'price_per_night',
            'price_bed_breakfast', 'price_halfboard', 'price_fullboard',
            'description', 'features', 'image'
        ]  # Added executive pricing fields

        widgets = {
            'room_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter room number'}),
            'room_type': forms.Select(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'price_per_night': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'price_bed_breakfast': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Enter price for Bed & Breakfast'}),
            'price_halfboard': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Enter price for Halfboard'}),
            'price_fullboard': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Enter price for Fullboard'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter room description'}),
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