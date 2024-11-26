from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
import uuid

# Create your models here.

#TODO create user role field for general user vs admin @InfiniteWes

class CustomUserManager(UserManager):
    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        # Remove username from extra_fields if it exists
        extra_fields.pop('username', None)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, name, password, **extra_fields)

    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not name:
            raise ValueError('The Name field must be set')

        email = self.normalize_email(email)
        
        # Remove username from extra_fields if it exists
        extra_fields.pop('username', None)
        
        # Generate username from email
        base_username = email.split('@')[0]
        username = base_username
        counter = 1
        
        # Ensure unique username
        while self.model.objects.filter(username=username).exists():
            username = f"{base_username}_{counter}"
            counter += 1
        
        user = self.model(
            email=email,
            name=name,
            username=username,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(
        max_length=150, 
        unique=True, 
        default=''
    )
    address = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
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
    tickets = models.ManyToManyField('BookingApp.Booking', related_name='ticket_holders', blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def save(self, *args, **kwargs):
        if not self.username:
            # Generate a unique username based on email
            base_username = self.email.split('@')[0]
            username = base_username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}_{counter}"
                counter += 1
            self.username = username
        super().save(*args, **kwargs)

    def __str__(self):
        return f"User {self.user_id}: {self.name}"

    class Meta:
        swappable = 'AUTH_USER_MODEL'

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
            # Don't compare raw passwords directly!
            user = cls.objects.get(email=email)
            # Use Django's built-in password verification
            from django.contrib.auth import authenticate
            if authenticate(email=email, password=password):
                return True
            return False
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