from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import User
import json

@method_decorator(csrf_exempt, name='dispatch')
class RegisterUserView(View):
    def post(self, request, *args, **kwargs):
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            
            # Extract required fields
            name = data.get('name')
            email = data.get('email')
            password = data.get('password')  # Note: Should be hashed in production
            address = data.get('address')
            phone = data.get('phone')
            
            # Validate required fields
            if not all([name, email, password, address, phone]):
                return JsonResponse({
                    'success': False,
                    'error': 'Missing required fields'
                }, status=400)
            
            # Validate phone number length
            if len(phone) != 10:
                return JsonResponse({
                    'success': False,
                    'error': 'Phone number must be 10 digits'
                }, status=400)
            
            # Attempt to register user
            success = User.register_user(
                name=name,
                email=email,
                password=password,
                address=address,
                phone_number=phone
            )
            
            if success:
                return JsonResponse({
                    'success': True,
                    'message': 'User registered successfully'
                }, status=201)
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Email already exists or registration failed'
                }, status=400)
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON'
            }, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class LoginUserView(View):
    def post(self, request, *args, **kwargs):
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            
            # Extract login credentials
            email = data.get('email')
            password = data.get('password')  # Note: Should be hashed in production
            
            # Validate required fields
            if not all([email, password]):
                return JsonResponse({
                    'success': False,
                    'error': 'Missing email or password'
                }, status=400)
            
            # Attempt to login
            success = User.login(email=email, password=password)
            
            if success:
                # Get user details
                user = User.objects.get(email=email)
                user_details = User.get_user_details(user.user_id)
                
                return JsonResponse({
                    'success': True,
                    'message': 'Login successful',
                    'user': user_details
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid email or password'
                }, status=401)
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON'
            }, status=400)