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
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import ensure_csrf_cookie
from uuid import UUID

@ensure_csrf_cookie
@login_required
@api_view(['POST'])
def create_booking(request):
    try:
        data = request.data
        user_id = data.get('user_id')
        showtime_id = data.get('showtime_id')
        ticket_count = data.get('ticket_count')
        total_price = data.get('total_price')
        ticket_id = data.get('ticket_id')
        show_date = data.get('showDate')
        show_time = data.get('showTime')
        theater_location = data.get('theaterLocation')

        print(f"Creating booking with data: {data}")
        print(f"Authenticated user: {request.user.pk}")

        # Validate required fields
        if not all([user_id, showtime_id, ticket_count, total_price, ticket_id]):
            return Response({'success': False, 'error': 'Missing required fields'}, status=400)

        # Convert ticket_id to UUID
        try:
            barcode = UUID(ticket_id)
        except ValueError:
            return Response({'success': False, 'error': 'Invalid ticket ID format'}, status=400)

        # Verify the authenticated user matches the user_id
        if request.user.pk != int(user_id):
            return Response({'success': False, 'error': 'Unauthorized'}, status=403)

        # Get the showtime and its related theater information
        showtime = Showtime.objects.get(pk=showtime_id)
        theater_location = data.get('theaterLocation') or showtime.theater.location  # Fallback to showtime's theater location
        
        # Create the booking
        booking = Booking.objects.create(
            user=request.user,
            showtime=showtime,
            ticket_count=ticket_count,
            total_price=Decimal(str(total_price)),
            barcode=barcode
        )
        
        print(f"Booking created with ID: {booking.booking_id}")

        return Response({
            'success': True,
            'booking': {
                'booking_id': booking.booking_id,
                'ticket_id': str(booking.barcode),
                'created_at': booking.created_at.isoformat(),
                'movie_title': showtime.movie.title,
                'show_date': show_date,
                'show_time': show_time,
                'theater_location': theater_location,
                'ticket_count': booking.ticket_count,
                'total_price': str(booking.total_price)
            }
        }, status=201)

    except Exception as e:
        print(f"Error creating booking: {str(e)}")
        print(f"Exception type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return Response({'success': False, 'error': str(e)}, status=500)


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

@login_required
def get_user_tickets(request, user_id):
    if request.method != 'GET':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

    try:
        print(f"Getting tickets for user {user_id}")
        
        # Get all bookings for the user through the ForeignKey relationship
        bookings = Booking.objects.filter(user_id=user_id).order_by('-created_at')
        print(f"Found {bookings.count()} bookings")
        
        bookings_data = []
        for booking in bookings:
            try:
                showtime = booking.showtime
                movie = showtime.movie
                theater = showtime.theater
                
                booking_data = {
                    'booking_id': booking.booking_id,
                    'movie_title': movie.title,
                    'show_date': showtime.show_date.isoformat(),
                    'show_time': showtime.show_time.strftime('%H:%M'),
                    'theater_location': f"{theater.name} - {theater.location}",
                    'ticket_count': booking.ticket_count,
                    'total_price': str(booking.total_price),
                    'barcode': str(booking.barcode),
                    'created_at': booking.created_at.isoformat()
                }
                bookings_data.append(booking_data)
                
            except AttributeError as e:
                print(f"Error processing booking {booking.booking_id}: {str(e)}")
                continue

        return JsonResponse({
            'success': True,
            'bookings': bookings_data,
            'debug_info': {
                'user_id': user_id,
                'auth_user_id': request.user.pk,
                'bookings_count': len(bookings_data)
            }
        })

    except Exception as e:
        print(f"Error in get_user_tickets: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
