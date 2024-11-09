# BookingApp/views.py
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Booking
from ShowtimeApp.models import Showtime
from UserApp.models import User
import json
from decimal import Decimal

@csrf_exempt
@login_required
def create_booking(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        showtime_id = data.get('showtime_id')
        ticket_count = data.get('ticket_count')
        total_price = data.get('total_price')

        # Validate required fields
        if not all([user_id, showtime_id, ticket_count, total_price]):
            return JsonResponse({'success': False, 'error': 'Missing required fields'}, status=400)

        # Retrieve user and showtime
        user = get_object_or_404(User, pk=int(user_id))
        showtime = get_object_or_404(Showtime, pk=int(showtime_id))

        ticket_count = int(ticket_count)
        if ticket_count < 1:
            return JsonResponse({'success': False, 'error': 'ticket_count must be at least 1'}, status=400)

        with transaction.atomic():
            # Lock the showtime record to prevent race conditions
            showtime = Showtime.objects.select_for_update().get(pk=showtime_id)

            if showtime.available_seats < ticket_count:
                return JsonResponse({'success': False, 'error': 'Not enough available seats'}, status=400)

            # Calculate total price
            total_price = Decimal(ticket_count) * showtime.ticket_price

            # Create booking
            booking = Booking.objects.create(
                user=user,
                showtime=showtime,
                ticket_count=ticket_count,
                total_price=total_price  # Set total_price explicitly
            )

            # Update available seats
            showtime.available_seats -= ticket_count
            showtime.save()

        # Prepare response data
        response_data = {
            'booking_id': booking.booking_id,
            'user_id': booking.user.id,
            'showtime_id': booking.showtime.id,
            'ticket_count': booking.ticket_count,
            'total_price': booking.total_price,  # Ensure it's a string for JSON serialization
            'barcode': str(booking.barcode),
            'created_at': booking.created_at.isoformat()
        }
        return JsonResponse({'success': True, 'booking': response_data}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'}, status=400)
    except ValueError:
        return JsonResponse({'success': False, 'error': 'Invalid data format'}, status=400)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User does not exist'}, status=404)
    except Showtime.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Showtime does not exist'}, status=404)
    except Exception as e:
        # Log the exception if logging is set up
        return JsonResponse({'success': False, 'error': 'An unexpected error occurred'}, status=500)


@csrf_exempt
@login_required
def cancel_booking(request, booking_id):
    if request.method != 'DELETE':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

    try:
        with transaction.atomic():
            # Lock the booking record to prevent race conditions
            booking = Booking.objects.select_for_update().get(booking_id=booking_id)

            # Restore available seats
            showtime = booking.showtime
            showtime.available_seats += booking.ticket_count
            showtime.save()

            # Delete the booking
            booking.delete()

        return JsonResponse({'success': True, 'message': 'Booking canceled successfully'}, status=200)

    except Booking.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Booking does not exist'}, status=404)
    except Exception as e:
        # Log the exception if logging is set up
        return JsonResponse({'success': False, 'error': 'An unexpected error occurred'}, status=500)


@login_required
def get_booking_details(request, booking_id):
    if request.method != 'GET':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

    try:
        booking = get_object_or_404(Booking, booking_id=booking_id)

        response_data = {
            'booking_id': booking.booking_id,
            'user_id': booking.user.id,
            'showtime_id': booking.showtime.id,
            'ticket_count': booking.ticket_count,
            'total_price': str(booking.total_price),
            'barcode': str(booking.barcode),
            'created_at': booking.created_at.isoformat()
        }

        return JsonResponse({'success': True, 'booking': response_data}, status=200)

    except Booking.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Booking does not exist'}, status=404)
    except Exception as e:
        # Log the exception if logging is set up
        return JsonResponse({'success': False, 'error': 'An unexpected error occurred'}, status=500)
