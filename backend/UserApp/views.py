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
            
            # Extract basic fields
            name = data.get('name')
            email = data.get('email')
            password = data.get('password')
            address = data.get('address')
            phone = data.get('phone')
            
            # Extract payment information
            payment_type = data.get('payment_type')
            payment_info = None
            
            if payment_type:
                if payment_type == 'credit_card':
                    # Validate credit card fields
                    card_number = data.get('card_number')
                    expiration_date = data.get('expiration_date')
                    cvv = data.get('cvv')
                    billing_address = data.get('billing_address')
                    
                    if not all([card_number, expiration_date, cvv, billing_address]):
                        return JsonResponse({
                            'success': False,
                            'error': 'Missing credit card information'
                        }, status=400)
                    
                    if not (len(card_number) == 16 and len(cvv) == 3):
                        return JsonResponse({
                            'success': False,
                            'error': 'Invalid card number or CVV format'
                        }, status=400)
                    
                    payment_info = {
                        'type': 'credit_card',
                        'card_number': card_number,
                        'expiration_date': expiration_date,
                        'cvv': cvv,
                        'billing_address': billing_address
                    }
                elif payment_type == 'paypal':
                    payment_info = {
                        'type': 'paypal'
                    }
            
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
            
            # Attempt to register user with payment info
            success = User.register_user(
                name=name,
                email=email,
                password=password,
                address=address,
                phone_number=phone,
                payment_info=payment_info
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