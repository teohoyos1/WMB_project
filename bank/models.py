from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=100, blank=True, null=True)

class Bank(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Wallet(models.Model):
    bank_f = models.ForeignKey(Bank, on_delete=models.CASCADE)
    person_f = models.ForeignKey(Person, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=20, decimal_places=2)

class Payment_category(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name

class Movement_wallet(models.Model):
    wallet_f = models.ForeignKey(Bank, on_delete=models.CASCADE)
    record_date = models.DateTimeField('record date')
    before_value = models.DecimalField(max_digits=20, decimal_places=2)
    actual_value = models.DecimalField(max_digits=20, decimal_places=2)
    type_movement = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    payment_category_f = models.ForeignKey(Payment_category, on_delete=models.CASCADE)

class Integration_data(models.Model):
    person_f = models.ForeignKey(Person, on_delete=models.CASCADE)
    token = models.CharField(max_length=200)
    creation_date = models.DateField(default=timezone.now)