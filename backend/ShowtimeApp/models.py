from django.db import models
from MovieApp.models import Movie  # Importing Movie model from MovieApp

class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)  # Link to the movie being shown
    theater_location = models.CharField(max_length=100)  # Location of the theater
    show_date = models.DateField()  # Date of the show
    show_time = models.TimeField()  # Time of the show
    ticket_price = models.DecimalField(max_digits=6, decimal_places=2)  # Price per ticket

    def add_showtime(cls, movie_id, theater_location, show_date, show_time, ticket_price):
        try:
            if cls.objects.filter(movie_id=movie_id, theater_location=theater_location, show_date=show_date, show_time=show_time).exists():
                return False
            
            showtime = cls.objects.create(
                movie_id=movie_id,
                theater_location=theater_location,
                show_date=show_date,
                show_time=show_time,
                ticket_price=ticket_price
            )
            return True
        except Exception:
            return False
        
    def update_showtime(cls, showtime_id, **kwargs):
        try:
            showtime = cls.objects.get(showtime_id=showtime_id)
            for key, value in kwargs.items():
                setattr(showtime, key, value)
            showtime.save()
            return True
        except cls.DoesNotExist:
            return False
    
    def delete_showtime(cls, showtime_id):
        try:
            showtime = cls.objects.get(showtime_id=showtime_id)
            showtime.delete()
            return True
        except cls.DoesNotExist:
            return False
        
    def get_showtimes_by_movie(cls, movie_id):
        try:
            showtimes = cls.objects.filter(movie_id=movie_id)
            return showtimes
        except cls.DoesNotExist:
            return None
    