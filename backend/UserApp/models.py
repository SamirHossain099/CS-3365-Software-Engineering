from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.IntegerField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    is_admin = models.BooleanField(default=False)

    def register_user(cls, name, email, password, address, phone_number):
        try:
            if cls.objects.filter(email=email).exists():
                return False
            
            user = cls.objects.create(
                name=name,
                email=email,
                password=password,
                address=address,
                phone=phone_number
            )
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
            return {
                'user_id': user.user_id,
                'name': user.name,
                'email': user.email,
                'address': user.address,
                'phone': user.phone,
                'is_admin': user.is_admin
            }
        except cls.DoesNotExist:
            return None
