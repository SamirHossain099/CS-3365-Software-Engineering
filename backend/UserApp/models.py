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