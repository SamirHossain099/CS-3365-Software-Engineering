from django.db import models

class Movie(models.Model):
    movie_id = models.IntegerField(primary_key=True)           # Primary key movie id
    title = models.CharField(max_length=255)                   # Movie title       
    genre = models.CharField(max_length=100)                   # Movie genre  
    duration = models.IntegerField()                           # Movie duration in minutes
    release_date = models.CharField(max_length=100)            # Movie release date
    description = models.TextField()                           # Movie description
    rating = models.FloatField()                               # Average rating out of 5
    image = models.ImageField(upload_to='movies/', null=True, blank=True)  # Movie image
    location = models.CharField(max_length=255, null=True, blank=True)     # Movie location
    director = models.CharField(max_length=225)
    imdb_rating = models.DecimalField(max_digits=3, decimal_places=1)

    def add_movie(cls, title, genre, duration, release_date, description, image=None, location=None): # Returns movie_id
        try:
            if cls.objects.filter(title=title).exists():
                return False
            
            movie = cls.objects.create(
                title=title,
                genre=genre,
                duration=duration,
                release_date=release_date,
                description=description,
                image=image,
                location=location
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