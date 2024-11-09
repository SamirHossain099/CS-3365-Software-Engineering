from django.db import models
from MovieApp.models import Movie  # Importing Movie model from MovieApp

class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)  # Link to the movie being shown
    theater_location = models.CharField(max_length=100)  # Location of the theater
    show_date = models.DateField()  # Date of the show
    show_time = models.TimeField()  # Time of the show
    ticket_price = models.DecimalField(max_digits=6, decimal_places=2)  # Price per ticket

    def __str__(self):
        return f"{self.movie.title} at {self.theater_location} on {self.show_date} at {self.show_time}"
