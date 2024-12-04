from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import User
import json
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

def is_admin(user):
    return user.is_authenticated and user.is_staff

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
                if payment_type in ['credit_card', 'debit_card']:
                    # Validate card fields
                    card_number = data.get('card_number')
                    expiration_date = data.get('expiration_date')
                    cvv = data.get('cvv')
                    billing_address = data.get('billing_address')
                    
                    if not all([card_number, expiration_date, cvv, billing_address]):
                        return JsonResponse({
                            'success': False,
                            'error': f'Missing {payment_type} information'
                        }, status=400)
                    
                    if not (len(card_number) == 16 and len(cvv) == 3):
                        return JsonResponse({
                            'success': False,
                            'error': 'Invalid card number or CVV format'
                        }, status=400)
                    
                    payment_info = {
                        'type': payment_type,
                        'card_number': card_number,
                        'expiration_date': expiration_date,
                        'cvv': cvv,
                        'billing_address': billing_address
                    }
                elif payment_type == 'paypal':
                    paypal_email = data.get('paypal_email')
                    if not paypal_email:
                        return JsonResponse({
                            'success': False,
                            'error': 'Missing PayPal email'
                        }, status=400)
                    
                    payment_info = {
                        'type': 'paypal',
                        'paypal_email': paypal_email
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
                # Get the newly created user
                user = User.objects.get(email=email)
                return JsonResponse({
                    'success': True,
                    'message': 'User registered successfully',
                    'user': {
                        'id': user.user_id,
                        'email': user.email,
                        'name': user.name
                    }
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
class LoginUserView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            
            if not email or not password:
                return Response(
                    {'error': 'Email and password are required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = authenticate(request, email=email, password=password)
            
            # Add debug logging
            print(f"Login attempt for email: {email}")
            print(f"User authenticated: {user is not None}")
            
            if user is not None:
                login(request, user)
                return Response({
                    'user': {
                        'id': user.user_id,
                        'email': user.email,
                        'name': user.name
                    }
                }, status=status.HTTP_200_OK)
            else:
                # Check if user exists to provide better error message
                user_exists = User.objects.filter(email=email).exists()
                error_msg = 'Invalid password' if user_exists else 'User not found'
                return Response(
                    {'error': error_msg}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
                
        except Exception as e:
            print(f"Login error: {str(e)}")  # For debugging
            return Response(
                {'error': 'Server error'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@csrf_exempt
@user_passes_test(is_admin)
def get_all_users(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        users = User.objects.all()
        users_data = [{
            'user_id': user.user_id,
            'name': user.name,
            'email': user.email,
            'address': user.address,
            'phone': user.phone,
            'payment_methods': {
                'credit_card': {
                    'enabled': user.has_credit_card,
                    'details': {
                        'card_number': '*' * 12 + user.credit_card_number[-4:] if user.credit_card_number else None,
                        'expiration_date': user.credit_card_expiration,
                        'billing_address': user.credit_card_billing
                    } if user.has_credit_card else None
                },
                'debit_card': {
                    'enabled': user.has_debit_card,
                    'details': {
                        'card_number': '*' * 12 + user.debit_card_number[-4:] if user.debit_card_number else None,
                        'expiration_date': user.debit_card_expiration,
                        'billing_address': user.debit_card_billing
                    } if user.has_debit_card else None
                },
                'paypal': {
                    'enabled': user.has_paypal,
                    'details': {
                        'email': user.paypal_email
                    } if user.has_paypal else None
                }
            }
        } for user in users]
        
        return JsonResponse({
            'success': True,
            'users': users_data
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class UpdateUserView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            user_id = data.get('user_id')
            name = data.get('name')
            email = data.get('email')
            address = data.get('address')
            phone = data.get('phone')

            if not all([user_id, name, email, address, phone]):
                return JsonResponse({
                    'success': False,
                    'error': 'Missing required fields'
                }, status=400)
            
            if len(phone) != 10:
                return JsonResponse({
                    'success': False,
                    'error': 'Phone number must be 10 digits'
                }, status=400)
            
            user = User.objects.get(user_id=user_id)
            user.name = name
            user.email = email
            user.address = address
            user.phone = phone
            user.save()

            return JsonResponse({
                'success': True,
                'message': 'User information updated successfully'
            })
        except User.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'User not found'
            }, status=404)
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class UserDetailView(View):
    def get(self, request, user_id):
        try:
            user = User.objects.get(user_id=user_id)
            return JsonResponse({
                'user_id': user.user_id,
                'name': user.name,
                'email': user.email,
                'address': user.address,
                'phone_number': user.phone
            })
        except User.DoesNotExist:
            return JsonResponse({
                'error': 'User not found'
            }, status=404)