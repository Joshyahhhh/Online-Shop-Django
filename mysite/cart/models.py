from django.db import models
from django.contrib.auth.models import User
from myapp.models import Product
# Create your models here.

class OrderDetail(models.Model):
    customer_username = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    amount = models.IntegerField(null=True)
    stripe_payment_intent = models.CharField(max_length=200, null=True)
    has_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)