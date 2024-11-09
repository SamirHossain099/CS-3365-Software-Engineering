from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Booking
from .serializers import BookingSerializer
from django.shortcuts import get_object_or_404
from showtimes.models import Showtime
from users.models import User

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().order_by('-created_at')
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['delete'], url_path='cancel')
    def cancel_booking(self, request, pk=None):
        booking = self.get_object()
        success = Booking.cancel_booking(booking.booking_id)
        if success:
            return Response({'success': True, 'message': 'Booking canceled successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, 'message': 'Failed to cancel booking.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)')
    def bookings_by_user(self, request, user_id=None):
        user = get_object_or_404(User, pk=user_id)
        bookings = Booking.objects.filter(user=user).order_by('-created_at')
        serializer = self.get_serializer(bookings, many=True)
        return Response({'bookings': serializer.data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='showtime/(?P<showtime_id>[^/.]+)')
    def bookings_by_showtime(self, request, showtime_id=None):
        showtime = get_object_or_404(Showtime, pk=showtime_id)
        bookings = Booking.objects.filter(showtime=showtime).order_by('-created_at')
        serializer = self.get_serializer(bookings, many=True)
        return Response({'bookings': serializer.data}, status=status.HTTP_200_OK)
