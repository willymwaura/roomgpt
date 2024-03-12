
from django.db import models
from django.utils.timezone import now
from django.db import models


# Create your models here.

class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    class Meta:
        app_label = 'mainapp'

    def __str__(self):
        return self.email
    
    
class CreditBalance(models.Model):
    user_id = models.IntegerField(unique=True)
    balance = models.IntegerField(default=0)

    class Meta:
        app_label = 'mainapp'
    def __str__(self):
        return f"User ID: {self.user_id}, Balance: {self.balance}"

class ImageHistory(models.Model):
    user_id = models.IntegerField()
    image_url = models.URLField()

    class Meta:
        app_label = 'mainapp'
        
    def __str__(self):
        return self.image_url

class PaymentsActivated(models.Model):
    email=models.EmailField()
    phone=models.BigIntegerField()
    amount=models.IntegerField()

    class Meta:
        app_label = 'mainapp'


