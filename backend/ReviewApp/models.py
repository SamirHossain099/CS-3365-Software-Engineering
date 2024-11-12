from django.db import models
from UserApp.models import User  # Importing User model from UserApp
from MovieApp.models import Movie  # Importing Movie model from MovieApp

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)        # Link to the user who wrote the review
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)      # Link to the movie being reviewed
    rating = models.PositiveSmallIntegerField()                     # Rating out of 5, e.g., 1 to 5 stars
    review_text = models.TextField(blank=True)                      # Optional review text
    created_at = models.DateTimeField(auto_now_add=True)            # Timestamp for when the review was created
                                                                    # Implement review ID as the primary key
