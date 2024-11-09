from django.shortcuts import render, get_object_or_404, redirect
from .models import Review
from MovieApp.models import Movie
from django.contrib.auth.decorators import login_required, user_passes_test


def is_admin(user):
    return user.is_authenticated and user.is_staff  # Checks if the user is an admin

@login_required
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        review_text = request.POST.get('review_text', '')
        Review.objects.create(
            user=request.user,
            movie=movie,
            rating=rating,
            review_text=review_text
        )
        return redirect('movie_reviews', movie_id=movie.id)
    return render(request, 'ReviewApp/submit_review.html', {'movie': movie})

def get_reviews(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = Review.objects.filter(movie=movie).order_by('-created_at')
    return render(request, 'ReviewApp/movie_reviews.html', {'movie': movie, 'reviews': reviews})

def update_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        review_text = request.POST.get('review_text', '')
        review.rating = rating
        review.review_text = review_text
        review.save()
        return redirect('movie_reviews', movie_id=review.movie.id)
    return render(request, 'ReviewApp/update_review.html', {'review': review})

@user_passes_test(is_admin)
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    movie_id = review.movie.id
    review.delete()
    return redirect('movie_reviews', movie_id=movie_id)

