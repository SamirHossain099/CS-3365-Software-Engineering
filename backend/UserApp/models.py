from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)         # Create user ID
    name = models.CharField(max_length=100)              # Create the users name
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"User {self.user_id}: {self.name}"

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
