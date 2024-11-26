from django.contrib import admin
from django.db.models import Count
from .models import AdminLog
from UserApp.models import User
from MovieApp.models import Movie
from BookingApp.models import Booking
from ReviewApp.models import Review

@admin.register(AdminLog)
class AdminLogAdmin(admin.ModelAdmin):
    list_display = ('log_id', 'admin_id', 'action', 'timestamp')
    list_filter = ('admin_id', 'timestamp')
    search_fields = ('action', 'admin_id')
    ordering = ('-timestamp',)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        
        # User Statistics
        extra_context['total_users'] = User.objects.count()
        
        # Movie Statistics
        extra_context['total_movies'] = Movie.objects.count()
        extra_context['upcoming_movies'] = Movie.objects.filter(upcoming=True).count()
        extra_context['current_movies'] = Movie.objects.filter(upcoming=False).count()
        
        # Booking Statistics
        extra_context['total_bookings'] = Booking.objects.count()
        
        # Review Statistics
        extra_context['total_reviews'] = Review.objects.count()
        
        # Admin Activity Statistics
        admin_activity = AdminLog.objects.values('admin_id')\
            .annotate(action_count=Count('log_id'))\
            .order_by('-action_count')[:5]  # Top 5 most active admins
        extra_context['admin_activity'] = admin_activity

        return super().changelist_view(request, extra_context=extra_context)

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

