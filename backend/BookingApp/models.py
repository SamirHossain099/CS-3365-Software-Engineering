# BookingApp/models.py
from django.db import models
from UserApp.models import User  # Importing User model from UserApp
from ShowtimeApp.models import Showtime  # Importing Showtime model from ShowtimeApp
import uuid
from django.core.validators import MaxValueValidator

class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')  # Link to the user who made the booking
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name='bookings')  # Link to the showtime
    ticket_count = models.PositiveIntegerField(validators=[MaxValueValidator(10)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Removed editable=False
    barcode = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calculate total price before saving if not already set
        if not self.total_price:
            self.total_price = self.ticket_count * self.showtime.ticket_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking {self.booking_id} by {self.user.email}"
