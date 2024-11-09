from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Showtime
from .serializers import ShowtimeSerializer
from movies.models import Movie
from django.shortcuts import get_object_or_404

class ShowtimeViewSet(viewsets.ModelViewSet):
    queryset = Showtime.objects.all().order_by('-show_date', '-show_time')
    serializer_class = ShowtimeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        showtime = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(ShowtimeSerializer(showtime).data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        showtime = serializer.save()
        return Response(ShowtimeSerializer(showtime).data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='movie/(?P<movie_id>[^/.]+)')
    def showtimes_by_movie(self, request, movie_id=None):
        movie = get_object_or_404(Movie, pk=movie_id)
        showtimes = Showtime.objects.filter(movie=movie).order_by('-show_date', '-show_time')
        serializer = self.get_serializer(showtimes, many=True)
        return Response({'showtimes': serializer.data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='theater/(?P<theater_location>[^/.]+)')
    def showtimes_by_theater(self, request, theater_location=None):
        showtimes = Showtime.objects.filter(theater_location__icontains=theater_location).order_by('-show_date', '-show_time')
        serializer = self.get_serializer(showtimes, many=True)
        return Response({'showtimes': serializer.data}, status=status.HTTP_200_OK)
