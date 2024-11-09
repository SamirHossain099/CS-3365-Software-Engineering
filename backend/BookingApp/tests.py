from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ShowtimeApp.models import Showtime, Movie
from .models import Booking

User = get_user_model()

class BookingTests(TestCase):
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
            ticket_price='10.00',
            available_seats=100
        )
        self.client.login(email='testuser@example.com', password='testpassword')

    def test_create_booking(self):
        url = reverse('booking-create')
        data = {
            'showtime': self.showtime.id,
            'ticket_count': 2
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('booking-list'))
        self.assertEqual(Booking.objects.count(), 1)
        booking = Booking.objects.first()
        self.assertEqual(booking.ticket_count, 2)
        self.assertEqual(booking.total_price, 20.00)
        self.showtime.refresh_from_db()
        self.assertEqual(self.showtime.available_seats, 98)

    def test_cancel_booking(self):
        booking = Booking.objects.create(
            user=self.user,
            showtime=self.showtime,
            ticket_count=2,
            total_price=20.00
        )
        self.showtime.available_seats -= 2
        self.showtime.save()

        url = reverse('booking-cancel', args=[booking.booking_id])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('booking-list'))
        self.assertEqual(Booking.objects.count(), 0)
        self.showtime.refresh_from_db()
        self.assertEqual(self.showtime.available_seats, 100)

    def test_booking_list_view(self):
        Booking.objects.create(
            user=self.user,
            showtime=self.showtime,
            ticket_count=2,
            total_price=20.00
        )
        url = reverse('booking-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Movie')
        self.assertContains(response, 'Test Theater')
        self.assertContains(response, '2 tickets')

    def test_booking_form_invalid_ticket_count(self):
        url = reverse('booking-create')
        data = {
            'showtime': self.showtime.id,
            'ticket_count': 0  # Invalid ticket count
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)  # Form re-rendered
        self.assertFormError(response, 'form', 'ticket_count', 'At least one ticket must be booked.')
        self.assertEqual(Booking.objects.count(), 0)

    def test_booking_form_insufficient_seats(self):
        url = reverse('booking-create')
        data = {
            'showtime': self.showtime.id,
            'ticket_count': 200  # Exceeds available seats
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)  # Form re-rendered
        self.assertFormError(response, 'form', 'showtime', 'Not enough available seats.')
        self.assertEqual(Booking.objects.count(), 0)
