from django.db import models
from django.core.exceptions import ValidationError



class Feature(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    ROOM_TYPES = [
        ('SINGLE', 'Single'),
        ('DOUBLE', 'Double'),
        ('SUITE', 'Suite'),
    ]

    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    capacity = models.IntegerField()
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    price_bed_breakfast = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    price_halfboard = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    price_fullboard = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    features = models.ManyToManyField(Feature, blank=True)
    image = models.ImageField(upload_to='room_images/', blank=True, null=True, default='default_room.jpg')

    def is_available_for_dates(self, check_in, check_out):
        """Check if the room is available for the given dates."""
        overlapping_bookings = Booking.objects.filter(
            room=self,
            status='CONFIRMED',
            check_in_date__lt=check_out,
            check_out_date__gt=check_in
        )
        return not overlapping_bookings.exists()

    def __str__(self):
        return f"Room {self.room_number} ({self.room_type})"



class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    ]
    EXECUTIVE_CHOICES = [
        ('BED_ONLY', 'Bed Only'),
        ('BED_BREAKFAST', 'Bed and Breakfast'),
        ('HALFBOARD', 'Halfboard'),
        ('FULLBOARD', 'Fullboard'),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    customer_gender = models.CharField(max_length=10, choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('OTHER', 'Other')], default='MALE')
    customer_id = models.CharField(max_length=50, unique=True, default='TEMP_ID')
    executive_choice = models.CharField(max_length=20, choices=EXECUTIVE_CHOICES, default='BED_BREAKFAST')
    customer_phone = models.CharField(max_length=15, blank=True, null=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    guests = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    def clean(self):
        if self.check_out_date <= self.check_in_date:
            raise ValidationError("Check-out date must be after check-in date.")

        if self.guests > self.room.capacity:
            raise ValidationError(f"Number of guests exceeds the room capacity of {self.room.capacity}.")

        if not self.room.is_available_for_dates(self.check_in_date, self.check_out_date):
            raise ValidationError("The selected room is not available for the given dates.")

    def calculate_total_price(self):
        num_nights = (self.check_out_date - self.check_in_date).days
        if self.executive_choice == 'BED_ONLY':
            price_per_night = self.room.price_per_night
        elif self.executive_choice == 'BED_BREAKFAST':
            price_per_night = self.room.price_bed_breakfast
        elif self.executive_choice == 'HALFBOARD':
            price_per_night = self.room.price_halfboard
        elif self.executive_choice == 'FULLBOARD':
            price_per_night = self.room.price_fullboard
        else:
            price_per_night = self.room.price_per_night
        return self.room.price_per_night * num_nights

    def save(self, *args, **kwargs):
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking for Room {self.room.room_number} by {self.customer_name}"


class RoomPayment(models.Model):
    PAYMENT_METHODS = [
        ('CASH', 'Cash'),
        ('CARD', 'Card'),
        ('MPESA', 'Mpesa'),
    ]

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    is_paid = models.BooleanField(default=False)

    @staticmethod
    def process_payment(booking_id, amount, method):
        booking = Booking.objects.get(id=booking_id)
        RoomPayment.objects.create(
            booking=booking,
            amount=amount,
            payment_method=method,
            is_paid=True,
        )
        return "Payment successful"

    def __str__(self):
        return f"Payment for Booking {self.booking.id}: {self.amount}"