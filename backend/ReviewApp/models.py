from django.db import models

# Create your models here.
class Review(models.Model):
    review_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField(max_length=10)
    movie_id = models.IntegerField(max_length=10)
    rating = models.FloatField()
    review = models.TextField(max_length=1000)
    review_date = models.DateField()

    def add_review(user_id, movie_id, rating, review): int # Returns review_id
    def get_reviews_by_movie(movie_id): list
    def update_movie_review(review_id, **kwargs): bool