from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Booking
from ShowtimeApp.models import Showtime
from UserApp.models import User
from django.contrib.auth.decorators import login_required

@login_required
def create_booking(request, showtime_id):
    showtime = get_object_or_404(Showtime, id=showtime_id)
    if request.method == 'POST':
        ticket_count = int(request.POST.get('ticket_count', 1))
        total_price = ticket_count * showtime.ticket_price
        booking = Booking.objects.create(
            user=request.user,
            showtime=showtime,
            ticket_count=ticket_count,
            total_price=total_price
        )
        return redirect('booking_detail', booking_id=booking.id)
    return render(request, 'BookingApp/create_booking.html', {'showtime': showtime})

@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'BookingApp/booking_detail.html', {'booking': booking})
