from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from movies.models import Movie
from .models import Showtime

class ShowtimeTests(APITestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            title='Test Movie',
            genre='Action',
            duration=120,
            release_date='2024-01-01',
            description='A test movie.',
            rating=0.0
        )
        self.showtime_data = {
            'movie': self.movie.id,
            'theater_location': 'Test Theater',
            'show_date': '2024-05-01',
            'show_time': '18:00',
            'ticket_price': '10.00',
            'available_seats': 100
        }
        self.showtime = Showtime.objects.create(
            movie=self.movie,
            theater_location='Test Theater',
            show_date='2024-05-01',
            show_time='18:00',
            ticket_price='10.00',
            available_seats=100
        )

    def test_add_showtime(self):
        url = reverse('showtime-list')
        response = self.client.post(url, self.showtime_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Showtime.objects.count(), 2)
        self.assertEqual(Showtime.objects.last().theater_location, 'Test Theater')

    def test_update_showtime(self):
        url = reverse('showtime-detail', args=[self.showtime.showtime_id])
        updated_data = {
            'theater_location': 'Updated Theater',
            'ticket_price': '12.00'
        }
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.showtime.refresh_from_db()
        self.assertEqual(self.showtime.theater_location, 'Updated Theater')
        self.assertEqual(str(self.showtime.ticket_price), '12.00')

    def test_delete_showtime(self):
        url = reverse('showtime-detail', args=[self.showtime.showtime_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Showtime.objects.count(), 0)

    def test_get_showtimes_by_movie(self):
        url = reverse('showtime-showtimes-by-movie', args=[self.movie.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['showtimes']), 1)

    def test_get_showtimes_by_theater(self):
        url = reverse('showtime-showtimes-by-theater', args=['Test Theater'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['showtimes']), 1)
