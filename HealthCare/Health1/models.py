from django.db import models
from django.contrib.auth.models import User
# from .managers import MYmanager


class HealthProduct(models.Model):
    name=models.CharField(max_length=150)
    image=models.ImageField(upload_to="medicalimg")
    productprice=models.FloatField()
    productquantity=models.IntegerField()
    offer=models.CharField(max_length=20)

class Transaction(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    category=models.CharField(max_length=40)
    category_id=models.IntegerField()
    purchase_quan=models.IntegerField()
    date=models.DateTimeField(auto_now_add=True)
    # object=models.Manager()
    # product=MYmanager()

    

class PurchaseItem(models.Model):
    name = models.CharField(max_length = 100)
    amount = models.IntegerField()
    order_id = models.CharField(max_length = 100)
    razorpay_payment_id = models.CharField(max_length = 100,blank=True)
    paid = models.BooleanField(default=False)

