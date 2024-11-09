from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from showtimes.models import Showtime, Movie
from .models import Booking

class BookingTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            name='Test User',
            password='testpassword',
            address='123 Test St',
            phone_number='1234567890',
            role='user'
        )
        self.movie = Movie.objects.create(
            title='Test Movie',
            genre='Action',
            duration=120,
            release_date='2024-01-01',
            description='A test movie.',
            rating=0.0
        )
        self.showtime = Showtime.objects.create(
            movie=self.movie,
            theater_location='Test Theater',
            show_date='2024-05-01',
            show_time='18:00',
            ticket_price=10.00
        )
        self.booking_data = {
            'user': self.user.id,
            'showtime': self.showtime.id,
            'ticket_count': 2
        }

    def test_create_booking(self):
        url = reverse('booking-list')
        response = self.client.post(url, self.booking_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(Booking.objects.get().ticket_count, 2)

    def test_cancel_booking(self):
        booking = Booking.objects.create(
            user=self.user,
            showtime=self.showtime,
            ticket_count=2,
            total_price=20.00
        )
        url = reverse('booking-cancel-booking', args=[booking.booking_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Booking.objects.count(), 0)

    def test_get_bookings_by_user(self):
        Booking.objects.create(
            user=self.user,
            showtime=self.showtime,
            ticket_count=2,
            total_price=20.00
        )
        url = reverse('booking-bookings-by-user', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['bookings']), 1)

    def test_get_bookings_by_showtime(self):
        Booking.objects.create(
            user=self.user,
            showtime=self.showtime,
            ticket_count=2,
            total_price=20.00
        )
        url = reverse('booking-bookings-by-showtime', args=[self.showtime.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['bookings']), 1)
