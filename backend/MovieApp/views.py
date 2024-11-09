from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Movie
from ReviewApp.models import Review
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg
import json


def is_admin(request, user):
    return user.is_authenticated and user.is_staff

def get_movie_details(movie):
    return {
        'movie_id': movie.movie_id,
        'title': movie.title,
        'genre': movie.genre,
        'description': movie.description,
        'release_date': movie.release_date,
        'duration': movie.duration,
        'rating': movie.imdb_rating,
        'image': movie.image.url if movie.image else None,
        'location': movie.location
    }

def get_movie(movie_id):
    try:
        movie = Movie.objects.get(movie_id=movie_id)
        return get_movie_details(movie)
    except Movie.DoesNotExist:
        return None

def get_movie_reviews(request, movie_id):
    movie = get_movie(movie_id)
    if movie is None:
        return JsonResponse({'error': 'Movie not found'}, status=404)
    reviews = Review.objects.filter(movie_id=movie_id)
    review_list = [get_review_details(review) for review in reviews]
    return JsonResponse({'movie': movie, 'reviews': review_list})

def get_movie_list(request):
    movies = Movie.objects.all()
    movie_list = [get_movie_details(movie) for movie in movies]
    return JsonResponse({'movies': movie_list})

def get_review_details(review):
    return {
        'review_id': review.pk,
        'user': review.user.username,
        'rating': review.rating,
        'comment': review.comment,
        'created_at': review.created_at,
    }

@csrf_exempt
def add_movie(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    try:
        data = json.loads(request.body)
        required_fields = ['title', 'genre', 'duration', 'release_date', 'description', 'imdb_rating']
        if not all(field in data for field in required_fields):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        movie = Movie.objects.create(
            title=data['title'],
            genre=data['genre'],
            duration=data['duration'],
            release_date=data['release_date'],
            description=data['description'],
            imdb_rating=data['imdb_rating'],
            location=data.get('location'),
            image=request.FILES.get('image')
        )
        return JsonResponse({'movie_id': movie.movie_id})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def update_movie(request, movie_id):
    if request.method != 'PUT':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    try:
        data = json.loads(request.body)
        movie = Movie.objects.get(movie_id=movie_id)
        for key, value in data.items():
            if hasattr(movie, key):
                setattr(movie, key, value)
        movie.save()
        return JsonResponse({'success': True})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Movie.DoesNotExist:
        return JsonResponse({'error': 'Movie not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def delete_movie(request, movie_id):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    try:
        movie = Movie.objects.get(movie_id=movie_id)
        movie.delete()
        return JsonResponse({'success': True})
    except Movie.DoesNotExist:
        return JsonResponse({'error': 'Movie not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def update_rating(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    try:
        data = json.loads(request.body)
        movie_id = data.get('movie_id')
        new_rating = data.get('rating')
        if movie_id is None or new_rating is None:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        movie = Movie.objects.get(movie_id=movie_id)
        movie.imdb_rating = new_rating
        movie.save()
        return JsonResponse({'success': True})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Movie.DoesNotExist:
        return JsonResponse({'error': 'Movie not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

