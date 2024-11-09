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

    def register_user(name, email, password, address, phone_number): bool
    def login(email, password): bool
    def get_user_details(user_id):

