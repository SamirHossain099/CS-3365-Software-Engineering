from django.shortcuts import render
from django.views.generic import ListView, CreateView     # For class-based views
from django.views import View
from django.http import JsonResponse                      # For returning JSON responses
from django.views.decorators.csrf import csrf_exempt      # For handling CSRF exceptions
from django.utils.decorators import method_decorator
from .models import Admin_log
import json

# Create your views here.
class AdminLogListView(ListView):
    model = Admin_log

    def get(self, request, *args, **kwargs):
        logs = self.model.objects.all().order_by('-timestamp')                 # Retrieve all logs from database, ordered by timestamp
        data = list(logs.values('log_id', 'admin_id', 'action', 'timestamp'))  # Convert queryset to list of dictionaries with specific fields
        return JsonResponse({'logs': data}, safe=False)                        # Return JSON Response containing all logs

# View to create new admin logs
# @csrf_exempt decorator allows this endpoint to receive POST requests without CSRF token
@method_decorator(csrf_exempt, name='dispatch')
class AdminLogCreateView(View):
    def post(self, request, *args, **kwargs):
        try:
            # parse the incoming JSON data from request body
            data = json.loads(request.body)
            admin_id = data.get('admin_id')
            action = data.get('action')

            # Convert admin_id to int for validation
            try:
                admin_id = int(admin_id)
            except (TypeError, ValueError):
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid admin_id format'
                }, status=400)

            # validate that required fields are present
            if not all([admin_id, action]):
                return JsonResponse({
                    'success': False,
                    'error': 'Missing required fields'
                }, status=400) # return 400 bad request if validation fails
            
            # attempt to create the log entry using model method
            success = Admin_log.log_action(admin_id, action)

            if success:
                return JsonResponse({
                    'success': True,
                    'message': 'Log entry created successfully'
                }, status=201) # return 201 created if log entry is successfully created
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Failed to create log entry'
                }, status=500) # return 500 internal server error if log entry creation fails
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON data'
            }, status=400) # return 400 bad request if JSON data is invalid

class AdminLogsByAdminView(View):
    def get(self, request, admin_id, *args, **kwargs):
        logs = Admin_log.get_logs_by_admin(admin_id)
        data = list(logs.values('log_id', 'admin_id', 'action', 'timestamp'))
        return JsonResponse({'logs': data}, safe=False)
