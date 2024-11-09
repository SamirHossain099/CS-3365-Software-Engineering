from django.db import models

# Create your models here.
class Movie(models.Model):
    movie_id = models.IntegerField(max_length= 10, primary_key=True)
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    duration = models.IntegerField()
    release_date = models.CharField(max_length=100)
    description = models.TextField()
    rating = models.FloatField()

    def add_movie(cls, title, genre, duration, release_date, description): # Returns movie_id
        try:
            if cls.objects.filter(title=title).exists():
                return False
            
            movie = cls.objects.create(
                title=title,
                genre=genre,
                duration=duration,
                release_date=release_date,
                description=description
            )
            return True
        except Exception:
            return False

    def update_movie(cls, movie_id, **kwargs):
        try:
            movie = cls.objects.get(movie_id=movie_id)
            for key, value in kwargs.items():
                setattr(movie, key, value)
            movie.save()
            return True
        except cls.DoesNotExist:
            return False

    def delete_movie(cls, movie_id):
        try:
            movie = cls.objects.get(movie_id=movie_id)
            movie.delete()
            return True
        except cls.DoesNotExist:
            return False
        
    def get_movie_details(movie_id):
        try:
            movie = Movie.objects.get(movie_id=movie_id)
            return {
                'movie_id': movie.movie_id,
                'title': movie.title,
                'genre': movie.genre,
                'duration': movie.duration,
                'release_date': movie.release_date,
                'description': movie.description,
                'rating': movie.rating
            }
        except Movie.DoesNotExist:
            return None

    def update_rating(movie_id, new_rating):
        try:
            movie = Movie.objects.get(movie_id=movie_id)
            movie.rating = new_rating
            movie.save()
            return True
        except Movie.DoesNotExist:
            return False