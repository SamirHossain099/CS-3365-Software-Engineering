from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Showtime
from MovieApp.models import Movie
from django.contrib.auth.decorators import login_required, user_passes_test

def is_admin(user):
    return user.is_authenticated and user.is_staff  # Check if user is admin

def showtime_list(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    showtimes = Showtime.objects.filter(movie=movie)
    return render(request, 'ShowtimeApp/showtime_list.html', {'movie': movie, 'showtimes': showtimes})

@user_passes_test(is_admin)
def create_showtime(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        theater_location = request.POST.get('theater_location')
        show_date = request.POST.get('show_date')
        show_time = request.POST.get('show_time')
        ticket_price = request.POST.get('ticket_price')
        Showtime.objects.create(
            movie=movie,
            theater_location=theater_location,
            show_date=show_date,
            show_time=show_time,
            ticket_price=ticket_price
        )
        return redirect('showtime_list', movie_id=movie.id)
    return render(request, 'ShowtimeApp/create_showtime.html', {'movie': movie})

@user_passes_test(is_admin)
def delete_showtime(request, showtime_id):
    showtime = get_object_or_404(Showtime, id=showtime_id)
    movie_id = showtime.movie.id
    showtime.delete()
    return redirect('showtime_list', movie_id=movie_id)
