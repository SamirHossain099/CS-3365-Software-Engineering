from django.db import models

# Create your models here.

#TODO create user role field for general user vs admin @InfiniteWes

class User(models.Model):                                                       
    user_id = models.AutoField(primary_key=True)         # Create user ID
    name = models.CharField(max_length=100)              # Create the users name
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    has_credit_card = models.BooleanField(default=False)
    credit_card_number = models.CharField(max_length=16, null=True, blank=True)
    credit_card_expiration = models.DateField(null=True, blank=True)
    credit_card_cvv = models.CharField(max_length=3, null=True, blank=True)
    credit_card_billing = models.CharField(max_length=100, null=True, blank=True)
    has_debit_card = models.BooleanField(default=False)
    debit_card_number = models.CharField(max_length=16, null=True, blank=True)
    debit_card_expiration = models.DateField(null=True, blank=True)
    debit_card_cvv = models.CharField(max_length=3, null=True, blank=True)
    debit_card_billing = models.CharField(max_length=100, null=True, blank=True)
    has_paypal = models.BooleanField(default=False)
    paypal_email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"User {self.user_id}: {self.name}"
    
    @classmethod
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
                        'has_credit_card': True,
                        'credit_card_number': payment_info.get('card_number'),
                        'credit_card_expiration': payment_info.get('expiration_date'),
                        'credit_card_cvv': payment_info.get('cvv'),
                        'credit_card_billing': payment_info.get('billing_address')
                    })
                elif payment_info.get('type') == 'paypal':
                    user_data.update({
                        'has_paypal': True,
                        'paypal_email': payment_info.get('email')
                    })
            
            user = cls.objects.create(**user_data)
            return True
        except Exception as e:
            print(f"Registration error: {str(e)}")  # Add debugging
            return False

    @classmethod
    def login(cls, email, password):
        try:
            user = cls.objects.get(email=email, password=password)
            return True
        except cls.DoesNotExist:
            return False
        
    @classmethod
    def get_user_details(cls, user_id):
        try:
            user = cls.objects.get(user_id=user_id)
            details = {
                'user_id': user.user_id,
                'name': user.name,
                'email': user.email,
                'address': user.address,
                'phone': user.phone,
                'payment_methods': {
                    'credit_card': {
                        'enabled': user.has_credit_card,
                        'details': None
                    },
                    'debit_card': {
                        'enabled': user.has_debit_card,
                        'details': None
                    },
                    'paypal': {
                        'enabled': user.has_paypal,
                        'details': None
                    }
                }
            }
            
            if user.has_credit_card:
                details['payment_methods']['credit_card']['details'] = {
                    'card_number': '*' * 12 + user.credit_card_number[-4:],
                    'expiration_date': user.credit_card_expiration,
                    'billing_address': user.credit_card_billing
                }
            
            if user.has_debit_card:
                details['payment_methods']['debit_card']['details'] = {
                    'card_number': '*' * 12 + user.debit_card_number[-4:],
                    'expiration_date': user.debit_card_expiration,
                    'billing_address': user.debit_card_billing
                }
            
            if user.has_paypal:
                details['payment_methods']['paypal']['details'] = {
                    'email': user.paypal_email
                }
            
            return details
        except cls.DoesNotExist:
            return None