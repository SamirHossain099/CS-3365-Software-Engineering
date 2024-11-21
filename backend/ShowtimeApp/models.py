from django.db import models
from MovieApp.models import Movie
import uuid

class Showtime(models.Model):
    showtime_id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    show_date = models.DateField()
    show_time = models.TimeField()
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2)
    available_seats = models.PositiveIntegerField(default=100)

    def __str__(self):
        return f"{self.movie.title} on {self.show_date} {self.show_time}"


