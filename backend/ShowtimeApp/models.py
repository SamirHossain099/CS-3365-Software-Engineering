from django.db import models
from MovieApp.models import Movie  # Ensure you have a Movie app
import uuid

class Showtime(models.Model):
    showtime_id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    theater_location = models.CharField(max_length=255)
    show_date = models.DateField()
    show_time = models.TimeField()
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2)  # Use DecimalField for currency
    available_seats = models.PositiveIntegerField(default=100)  # Assuming a default seat count

    def __str__(self):
        return f"{self.movie.title} at {self.theater_location} on {self.show_date} {self.show_time}"

    @classmethod
    def add_showtime(cls, movie, theater_location, show_date, show_time, ticket_price, available_seats=100):
        try:
            showtime = cls.objects.create(
                movie=movie,
                theater_location=theater_location,
                show_date=show_date,
                show_time=show_time,
                ticket_price=ticket_price,
                available_seats=available_seats
            )
            return showtime
        except Exception as e:
            # Optionally, log the exception e
            return None

    @classmethod
    def update_showtime(cls, showtime_id, **kwargs):
        try:
            showtime = cls.objects.get(pk=showtime_id)
            for key, value in kwargs.items():
                setattr(showtime, key, value)
            showtime.save()
            return True
        except cls.DoesNotExist:
            return False
        except Exception:
            return False

    @classmethod
    def delete_showtime(cls, showtime_id):
        try:
            showtime = cls.objects.get(pk=showtime_id)
            showtime.delete()
            return True
        except cls.DoesNotExist:
            return False
        except Exception:
            return False

    @classmethod
    def get_showtime_details(cls, showtime_id):
        try:
            showtime = cls.objects.get(pk=showtime_id)
            return {
                'showtime_id': showtime.showtime_id,
                'movie': showtime.movie.title,
                'theater_location': showtime.theater_location,
                'show_date': showtime.show_date,
                'show_time': showtime.show_time,
                'ticket_price': showtime.ticket_price,
                'available_seats': showtime.available_seats,
            }
        except cls.DoesNotExist:
            return {}
