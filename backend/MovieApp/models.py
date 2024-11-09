from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)  # Auto-incrementing ID
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    duration = models.IntegerField()
    release_date = models.DateField()
    description = models.TextField()
    image = models.ImageField(upload_to='movies/', null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    director = models.CharField(max_length=225, null=True, blank=True)
    imdb_rating = models.DecimalField(
        max_digits=2, decimal_places=1,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )

    def __str__(self):
        return self.title