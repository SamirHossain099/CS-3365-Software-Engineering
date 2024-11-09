from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)         # Create user ID
    name = models.CharField(max_length=100)              # Create the users name
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    creditCardNumber = models.CharField(max_length=16, null=True, blank=True)
    expirationDate = models.DateField(null=True, blank=True)
    cvv = models.CharField(max_length=3, null=True, blank=True)
    billingAddress = models.CharField(max_length=100, default="Example Street", null=True, blank=True)
    isCreditCard = models.BooleanField(default=False)
    isPaypal = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"User {self.user_id}: {self.name}"

    def register_user(cls, name, email, password, address, phone_number, payment_info=None):
        try:
            if cls.objects.filter(email=email).exists():
                return False
            
            user_data = {
                'name': name,
                'email': email,
                'password': password,
                'address': address,
                'phone': phone_number
            }
            
            # Add payment information if provided
            if payment_info:
                if payment_info.get('type') == 'credit_card':
                    user_data.update({
                        'isCreditCard': True,
                        'creditCardNumber': payment_info.get('card_number'),
                        'expirationDate': payment_info.get('expiration_date'),
                        'cvv': payment_info.get('cvv'),
                        'billingAddress': payment_info.get('billing_address')
                    })
                elif payment_info.get('type') == 'paypal':
                    user_data.update({
                        'isPaypal': True
                    })
            
            user = cls.objects.create(**user_data)
            return True
        except Exception:
            return False

    def login(cls, email, password):
        try:
            user = cls.objects.get(email=email, password=password)
            return True
        except cls.DoesNotExist:
            return False
        
    def get_user_details(cls, user_id):
        try:
            user = cls.objects.get(user_id=user_id)
            details = {
                'user_id': user.user_id,
                'name': user.name,
                'email': user.email,
                'address': user.address,
                'phone': user.phone,
                'is_admin': user.is_admin,
                'payment_methods': {
                    'credit_card': user.isCreditCard,
                    'paypal': user.isPaypal
                }
            }
            
            if user.isCreditCard:
                details['credit_card'] = {
                    'card_number': '*' * 12 + user.creditCardNumber[-4:],  # Only show last 4 digits
                    'expiration_date': user.expirationDate,
                    'billing_address': user.billingAddress
                }
            
            return details
        except cls.DoesNotExist:
            return None
