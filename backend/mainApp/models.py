from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=200)                    # Username of the user
    password = models.CharField(max_length=200)                    # Password of the user
    email = models.EmailField(max_length=200)                      # Email of the user
    isAdmin = models.BooleanField(default=False)                   # Boolean to check if the user is an admin

class Movie(models.Model):
    title = models.CharField(max_length=200)                       # Title of the movie
    description = models.TextField()                               # Description for the movie
    cast = models.CharField(max_length=200)                        # Cast of the movie
    genre = models.CharField(max_length=200)                       # Genre of the movie
    rating = models.IntegerField()                                 # Rating of the movie

class Receipt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)       # Associated user
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)     # Movie choice
    date = models.DateField()                                      # Date of the movie
    time = models.TimeField()                                      # Time of the movie
    theater = models.CharField(max_length=200)                     # Theater name
    ticketCount = models.IntegerField()                            # number of tickets purchased
    price = models.FloatField()                                    # total price of the ticket(s)
