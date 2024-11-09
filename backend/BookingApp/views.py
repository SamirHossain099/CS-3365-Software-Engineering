from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Booking
from ShowtimeApp.models import Showtime
from django.contrib.auth import get_user_model
import json
from django.db import transaction

User = get_user_model()

# List all bookings
class BookingListView(View):
    def get(self, request, *args, **kwargs):
        bookings = Booking.objects.all().order_by('-created_at')
        data = list(bookings.values(
            'booking_id', 'user_id', 'showtime_id', 'ticket_count', 'total_price', 'barcode', 'created_at'
        ))
        return JsonResponse({'bookings': data}, safe=False)

# Create a new booking
@method_decorator(csrf_exempt, name='dispatch')
class BookingCreateView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            showtime_id = data.get('showtime_id')
            ticket_count = data.get('ticket_count')

            # Validate required fields
            if not all([user_id, showtime_id, ticket_count]):
                return JsonResponse({'success': False, 'error': 'Missing required fields'}, status=400)

            # Validate data types
            try:
                user = User.objects.get(pk=int(user_id))
            except (TypeError, ValueError, User.DoesNotExist):
                return JsonResponse({'success': False, 'error': 'Invalid user_id'}, status=400)

            try:
                showtime = Showtime.objects.get(pk=int(showtime_id))
            except (TypeError, ValueError, Showtime.DoesNotExist):
                return JsonResponse({'success': False, 'error': 'Invalid showtime_id'}, status=400)

            if int(ticket_count) < 1:
                return JsonResponse({'success': False, 'error': 'ticket_count must be at least 1'}, status=400)

            if showtime.available_seats < int(ticket_count):
                return JsonResponse({'success': False, 'error': 'Not enough available seats'}, status=400)

            with transaction.atomic():
                # Create booking
                booking = Booking.objects.create(
                    user=user,
                    showtime=showtime,
                    ticket_count=int(ticket_count),
                    total_price=int(ticket_count) * showtime.ticket_price
                )
                # Update available seats
                showtime.available_seats -= int(ticket_count)
                showtime.save()

            data = {
                'booking_id': booking.booking_id,
                'user_id': booking.user.id,
                'showtime_id': booking.showtime.id,
                'ticket_count': booking.ticket_count,
                'total_price': str(booking.total_price),
                'barcode': str(booking.barcode),
                'created_at': booking.created_at
            }
            return JsonResponse({'success': True, 'booking': data}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data'}, status=400)

# Retrieve bookings by user
class BookingsByUserView(View):
    def get(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(pk=int(user_id))
            bookings = Booking.objects.filter(user=user).order_by('-created_at')
            data = list(bookings.values(
                'booking_id', 'showtime_id', 'ticket_count', 'total_price', 'barcode', 'created_at'
            ))
            return JsonResponse({'bookings': data}, safe=False)
        except (TypeError, ValueError, User.DoesNotExist):
            return JsonResponse({'success': False, 'error': 'Invalid user_id'}, status=400)

# Cancel a booking
@method_decorator(csrf_exempt, name='dispatch')
class BookingCancelView(View):
    def post(self, request, booking_id, *args, **kwargs):
        try:
            booking = Booking.objects.get(pk=int(booking_id))
            with transaction.atomic():
                # Restore available seats
                booking.showtime.available_seats += booking.ticket_count
                booking.showtime.save()
                # Delete the booking
                booking.delete()
            return JsonResponse({'success': True, 'message': 'Booking canceled successfully'}, status=200)
        except (TypeError, ValueError, Booking.DoesNotExist):
            return JsonResponse({'success': False, 'error': 'Invalid booking_id'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': 'Failed to cancel booking'}, status=500)
