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

    @classmethod
    def create_booking(cls, user_id, showtime_id, ticket_count):
        """
        Create a new booking and calculate the total price based on ticket count and showtime ticket price.
        Returns the booking ID if successful, or -1 if there was an error.
        """
        try:
            user = User.objects.get(pk=user_id)
            showtime = Showtime.objects.get(pk=showtime_id)
            total_price = ticket_count * showtime.ticket_price  # Calculate total price

            booking = cls.objects.create(
                user=user,
                showtime=showtime,
                ticket_count=ticket_count,
                total_price=total_price
            )
            return booking.id
        except (User.DoesNotExist, Showtime.DoesNotExist):
            return -1  # Return -1 if there was an error with creating the booking

    def _generate_barcode(self):
        """
        Generate a unique barcode for the booking.
        This is a private method used internally to ensure each booking has a unique identifier.
        """
        return str(uuid.uuid4())  # UUID generates a unique string

    @classmethod
    def get_booking_details(cls, booking_id):
        """
        Get the details of a specific booking as a dictionary.
        Returns None if the booking does not exist.
        """
        try:
            booking = cls.objects.get(pk=booking_id)
            return {
                'booking_id': booking.id,
                'user_id': booking.user.id,
                'showtime_id': booking.showtime.id,
                'ticket_count': booking.ticket_count,
                'total_price': booking.total_price,
                'barcode': booking.barcode,
                'created_at': booking.created_at
            }
        except cls.DoesNotExist:
            return None

    @classmethod
    def cancel_booking(cls, booking_id):
        """
        Cancel a booking by deleting it from the database.
        Returns True if the booking was successfully deleted, or False if it does not exist.
        """
        try:
            booking = cls.objects.get(pk=booking_id)
            booking.delete()
            return True
        except cls.DoesNotExist:
            return False
