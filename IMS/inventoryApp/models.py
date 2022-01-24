from django.db import models

# Create your models here.
class Product(models.Model):
    itemNumber = models.CharField(max_length=11)
    itemName = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    expiry = models.CharField(max_length=30)
    quantity = models.FloatField()
    prize = models.CharField(max_length=30)
    notes = models.CharField(max_length=30)
    addDate = models.DateField(auto_now_add=True)