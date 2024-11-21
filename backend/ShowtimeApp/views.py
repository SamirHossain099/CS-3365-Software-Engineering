from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Showtime
from MovieApp.models import Movie
import json
from django.db import transaction
from django.utils import timezone

# List all showtimes
class ShowtimeListView(View):
    def get(self, request, *args, **kwargs):
        showtimes = Showtime.objects.all().order_by('-show_date', '-show_time')
        data = list(showtimes.values(
            'showtime_id', 'movie_id', 'show_date', 'show_time', 'ticket_price', 'available_seats'
        ))
        return JsonResponse({'showtimes': data}, safe=False)

# Create a new showtime
@method_decorator(csrf_exempt, name='dispatch')
class ShowtimeCreateView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            movie_id = data.get('movie_id')
            show_date = data.get('show_date')
            show_time = data.get('show_time')
            ticket_price = data.get('ticket_price')
            available_seats = data.get('available_seats', 100)  # Default to 100 if not provided

            # Validate required fields
            if not all([movie_id, show_date, show_time, ticket_price]):
                return JsonResponse({'success': False, 'error': 'Missing required fields'}, status=400)

            # Validate movie existence
            try:
                movie = Movie.objects.get(pk=int(movie_id))
            except (TypeError, ValueError, Movie.DoesNotExist):
                return JsonResponse({'success': False, 'error': 'Invalid movie_id'}, status=400)

            # Validate ticket_price and available_seats
            try:
                ticket_price = float(ticket_price)
                available_seats = int(available_seats)
                if ticket_price < 0 or available_seats < 0:
                    raise ValueError
            except (TypeError, ValueError):
                return JsonResponse({'success': False, 'error': 'Invalid ticket_price or available_seats'}, status=400)

            # Validate show_date and show_time
            try:
                show_date_obj = timezone.datetime.strptime(show_date, '%Y-%m-%d').date()
                show_time_obj = timezone.datetime.strptime(show_time, '%H:%M').time()
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Invalid date or time format'}, status=400)

            if show_date_obj < timezone.now().date() or (show_date_obj == timezone.now().date() and show_time_obj < timezone.now().time()):
                return JsonResponse({'success': False, 'error': 'Cannot create showtime for past dates/times'}, status=400)

            with transaction.atomic():
                # Create showtime
                showtime = Showtime.objects.create(
                    movie=movie,
                    show_date=show_date_obj,
                    show_time=show_time_obj,
                    ticket_price=ticket_price,
                    available_seats=available_seats
                )

            data = {
                'showtime_id': showtime.showtime_id,
                'movie_id': showtime.movie.id,
                'show_date': showtime.show_date,
                'show_time': showtime.show_time,
                'ticket_price': str(showtime.ticket_price),
                'available_seats': showtime.available_seats
            }
            return JsonResponse({'success': True, 'showtime': data}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data'}, status=400)

# Retrieve showtimes by movie
class ShowtimesByMovieView(View):
    def get(self, request, movie_id, *args, **kwargs):
        try:
            movie = Movie.objects.get(pk=int(movie_id))
            showtimes = Showtime.objects.filter(movie=movie).order_by('-show_date', '-show_time')
            data = list(showtimes.values(
                'showtime_id', 'show_date', 'show_time', 'ticket_price', 'available_seats'
            ))
            return JsonResponse({'showtimes': data}, safe=False)
        except (TypeError, ValueError, Movie.DoesNotExist):
            return JsonResponse({'success': False, 'error': 'Invalid movie_id'}, status=400)

# Retrieve showtimes by theater location
class ShowtimesByTheaterView(View):
    def get(self, request, theater_location, *args, **kwargs):
        showtimes = Showtime.objects.filter(theater_location__icontains=theater_location).order_by('-show_date', '-show_time')
        data = list(showtimes.values(
            'showtime_id', 'movie_id', 'show_date', 'show_time', 'ticket_price', 'available_seats'
        ))
        return JsonResponse({'showtimes': data}, safe=False)

# Update an existing showtime
@method_decorator(csrf_exempt, name='dispatch')
class ShowtimeUpdateView(View):
    def post(self, request, showtime_id, *args, **kwargs):
        try:
            showtime = Showtime.objects.get(pk=int(showtime_id))
            data = json.loads(request.body)

            # Extract fields to update
            movie_id = data.get('movie_id', showtime.movie.id)
            show_date = data.get('show_date', showtime.show_date.strftime('%Y-%m-%d'))
            show_time = data.get('show_time', showtime.show_time.strftime('%H:%M'))
            ticket_price = data.get('ticket_price', showtime.ticket_price)
            available_seats = data.get('available_seats', showtime.available_seats)

            # Validate movie existence
            try:
                movie = Movie.objects.get(pk=int(movie_id))
            except (TypeError, ValueError, Movie.DoesNotExist):
                return JsonResponse({'success': False, 'error': 'Invalid movie_id'}, status=400)

            # Validate ticket_price and available_seats
            try:
                ticket_price = float(ticket_price)
                available_seats = int(available_seats)
                if ticket_price < 0 or available_seats < 0:
                    raise ValueError
            except (TypeError, ValueError):
                return JsonResponse({'success': False, 'error': 'Invalid ticket_price or available_seats'}, status=400)

            # Validate show_date and show_time
            try:
                show_date_obj = timezone.datetime.strptime(show_date, '%Y-%m-%d').date()
                show_time_obj = timezone.datetime.strptime(show_time, '%H:%M').time()
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Invalid date or time format'}, status=400)

            if show_date_obj < timezone.now().date() or (show_date_obj == timezone.now().date() and show_time_obj < timezone.now().time()):
                return JsonResponse({'success': False, 'error': 'Cannot update showtime to past dates/times'}, status=400)

            with transaction.atomic():
                # Update showtime fields
                showtime.movie = movie
                showtime.show_date = show_date_obj
                showtime.show_time = show_time_obj
                showtime.ticket_price = ticket_price
                showtime.available_seats = available_seats
                showtime.save()

            data = {
                'showtime_id': showtime.showtime_id,
                'movie_id': showtime.movie.id,
                'show_date': showtime.show_date,
                'show_time': showtime.show_time,
                'ticket_price': str(showtime.ticket_price),
                'available_seats': showtime.available_seats
            }
            return JsonResponse({'success': True, 'showtime': data}, status=200)

        except (TypeError, ValueError, Showtime.DoesNotExist):
            return JsonResponse({'success': False, 'error': 'Invalid showtime_id'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data'}, status=400)

# Delete a showtime
@method_decorator(csrf_exempt, name='dispatch')
class ShowtimeDeleteView(View):
    def post(self, request, showtime_id, *args, **kwargs):
        try:
            showtime = Showtime.objects.get(pk=int(showtime_id))
            showtime.delete()
            return JsonResponse({'success': True, 'message': 'Showtime deleted successfully'}, status=200)
        except (TypeError, ValueError, Showtime.DoesNotExist):
            return JsonResponse({'success': False, 'error': 'Invalid showtime_id'}, status=400)
        except Exception:
            return JsonResponse({'success': False, 'error': 'Failed to delete showtime'}, status=500)
