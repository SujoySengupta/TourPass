from django.db import models
from django.conf import settings



class Museum(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField()
    location = models.CharField(max_length=200)
    opening_hour = models.TimeField(null=True, blank=True)
    closing_hour = models.TimeField(null=True, blank=True)
    closing_days = models.CharField(max_length=200, null=True, blank=True)
    image_location = models.CharField(max_length=200, null=True, blank=True)
    price_per_ticket = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        null=True,
        blank=True,
        help_text="In units of currency, e.g., INR."
    )
    def __str__(self):
        return self.name
    
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
    booking_date = models.DateTimeField(auto_now_add=True)
    visit_date = models.DateField(null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Booking #{self.id} by {self.user.username} for {self.museum.name}"

    @property
    def total_price(self):
        if self.museum.price_per_ticket:
            return self.quantity * self.museum.price_per_ticket
        return 0