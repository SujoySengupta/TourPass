from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings



class Museum(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField()
    location = models.CharField(max_length=200)
    opening_hour = models.CharField(max_length=100)
    image_location = models.CharField(max_length=200,null=True,blank=True)
    price_per_ticket = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        null=True,
        blank = True,
        help_text="In units of currency, e.g., INR."
    )
    def __str__(self):
        return self.name
    
class TimeSlot(models.Model):
    museum = models.ForeignKey(Museum,on_delete=models.CASCADE,related_name='time_slots')
    date = models.DateField()
    time_start = models.TimeField()
    time_end = models.TimeField()
    total_tickets = models.PositiveBigIntegerField()
    remaining_tickets = models.PositiveBigIntegerField()
    

    def __str__(self):
        return (
            f"{self.museum.name} - {self.date} "
            f"({self.time_start} - {self.time_end})"
        )
    
    def book_tickets(self, quantity):
        """
        Helper method to reduce remaining tickets by quantity.
        Add any logic for preventing over-booking, etc.
        """
        if quantity > self.remaining_tickets:
            raise ValueError("Not enough tickets available.")
        self.remaining_tickets -= quantity
        self.save()

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='bookings'
    )
    museum = models.ForeignKey(
        Museum, 
        on_delete=models.CASCADE, 
        related_name='bookings'
    )
    timeslot = models.ForeignKey(
        TimeSlot, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    quantity = models.PositiveIntegerField(default=1)
    booking_date = models.DateTimeField(auto_now_add=True)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Booking #{self.id} by {self.user.username} for {self.museum.name}"

    @property
    def total_price(self):
        """
        Return the total amount (INR) for this booking.
        If timeslot or museum has a price, multiply by quantity, etc.
        """
        if self.timeslot and self.museum.price_per_ticket:
            return self.quantity * self.museum.price_per_ticket
        return 0