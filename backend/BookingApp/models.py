from django.db import models
from django.contrib.auth import get_user_model
from showtimes.models import Showtime
import uuid

User = get_user_model()

class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name='bookings')
    ticket_count = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    barcode = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.booking_id} by {self.user.email}"

    def calculate_total_price(self):
        return self.ticket_count * self.showtime.ticket_price

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)

    @classmethod
    def create_booking(cls, user, showtime, ticket_count):
        try:
            booking = cls.objects.create(
                user=user,
                showtime=showtime,
                ticket_count=ticket_count,
                total_price=ticket_count * showtime.ticket_price
            )
            return booking
        except Exception as e:
            # Optionally, log the exception e
            return None

    @classmethod
    def cancel_booking(cls, booking_id):
        try:
            booking = cls.objects.get(pk=booking_id)
            booking.delete()
            return True
        except cls.DoesNotExist:
            return False
        except Exception:
            return False
