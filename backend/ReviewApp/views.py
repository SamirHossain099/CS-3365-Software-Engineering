from django.shortcuts import render, get_object_or_404, redirect
from .models import Review
from MovieApp.models import Movie
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from UserApp.models import User

def is_admin(user):
    return user.is_authenticated and user.is_staff  # Checks if the user is an admin

@csrf_exempt
def add_review(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        print("Received data:", data)  # Debug print
        
        movie_id = data.get('movie_id')
        user_id = data.get('user_id')
        rating = data.get('rating')
        review_text = data.get('review_text')
        
        # Validate all required fields
        if not all([movie_id, user_id, rating, review_text]):
            return JsonResponse({
                'error': 'Missing required fields',
                'received': {
                    'movie_id': movie_id,
                    'user_id': user_id,
                    'rating': rating,
                    'review_text': review_text
                }
            }, status=400)
            
        # Get the movie and user objects
        try:
            movie = Movie.objects.get(movie_id=movie_id)
            user = User.objects.get(user_id=user_id)
        except Movie.DoesNotExist:
            return JsonResponse({'error': f'Movie with id {movie_id} not found'}, status=404)
        except User.DoesNotExist:
            return JsonResponse({'error': f'User with id {user_id} not found'}, status=404)
        
        # Create the review
        review = Review.objects.create(
            user=user,
            movie=movie,
            rating=rating,
            review_text=review_text
        )
        
        return JsonResponse({
            'success': True,
            'review_id': review.id
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        print("Error creating review:", str(e))  # Debug print
        return JsonResponse({'error': str(e)}, status=400)

def get_reviews(request, movie_id):
    movie = get_object_or_404(Movie, movie_id=movie_id)
    reviews = Review.objects.filter(movie=movie).order_by('-created_at')
    reviews_data = [{
        'review_id': review.id,
        'user_id': review.user.user_id,
        'user_name': review.user.name,
        'rating': review.rating,
        'review_text': review.review_text,
        'created_at': review.created_at.isoformat()
    } for review in reviews]
    return JsonResponse({
        'movie_id': movie.movie_id,
        'movie_title': movie.title,
        'reviews': reviews_data
    })

@csrf_exempt
def update_review(request, review_id):
    if request.method != 'PUT':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    review = get_object_or_404(Review, id=review_id)
    try:
        data = json.loads(request.body)
        review.rating = data.get('rating', review.rating)
        review.review_text = data.get('review_text', review.review_text)
        review.save()
        return JsonResponse({'success': True})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@user_passes_test(is_admin)
def delete_review(request, review_id):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    review = get_object_or_404(Review, id=review_id)
    review.delete()
    return JsonResponse({'success': True})

