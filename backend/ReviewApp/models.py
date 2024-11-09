from django.db import models
from UserApp.models import User  # Importing User model from UserApp
from MovieApp.models import Movie  # Importing Movie model from MovieApp

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)        # Link to the user who wrote the review
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)      # Link to the movie being reviewed
    rating = models.PositiveSmallIntegerField()                     # Rating out of 5, e.g., 1 to 5 stars
    review_text = models.TextField(blank=True)                      # Optional review text
    created_at = models.DateTimeField(auto_now_add=True)            # Timestamp for when the review was created

    def add_review(cls, user_id, movie_id, rating, review_text):
        try:
            user = User.objects.get(user_id=user_id)
            movie = Movie.objects.get(movie_id=movie_id)
            review = cls.objects.create(
                user=user,
                movie=movie,
                rating=rating,
                review_text=review_text
            )
            return True
        except Exception:
            return False
    
    def update_review(cls, review_id, **kwargs):
        try:
            review = cls.objects.get(review_id=review_id)
            for key, value in kwargs.items():
                setattr(review, key, value)
            review.save()
            return True
        except cls.DoesNotExist:
            return False
        
    def get_reviews_by_movie(cls, movie_id):
        try:
            reviews = cls.objects.filter(movie_id=movie_id)
            return [{
                'review_id': review.id,
                'user_id': review.user.id,
                'user_name': review.user.username,
                'rating': review.rating,
                'review_text': review.review_text,
                'created_at': review.created_at
            } for review in reviews]
        except cls.DoesNotExist:
            return None
