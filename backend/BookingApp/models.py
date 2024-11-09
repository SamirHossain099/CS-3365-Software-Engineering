from django.db import models
from UserApp.models import User  # Importing User model from UserApp
from ShowtimeApp.models import Showtime  # Importing Showtime model from ShowtimeApp
import uuid

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to User who made the booking
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)  # Link to the Showtime booked
    ticket_count = models.PositiveIntegerField()  # Number of tickets booked
    total_price = models.DecimalField(max_digits=6, decimal_places=2)  # Total price for the booking
    barcode = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)  # Unique booking barcode
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the booking was created

    def __str__(self):
        return f"Booking {self.barcode} for {self.user}"

    def save(self, *args, **kwargs):
        # Calculate total_price before saving
        if not self.total_price:
            self.total_price = self.ticket_count * self.showtime.ticket_price
        super().save(*args, **kwargs)
