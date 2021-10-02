from django.db import models
from django.shortcuts import render

# Create your models here.
class ProdeuctModel(models.Model):
    pname=models.CharField(max_length=100,default='')
    pprice=models.IntegerField(default=0)
    pimages=models.CharField(max_length=100,default='')
    pdescription=models.TextField(blank=True,default='')
    def __str__(self):
        return self.pname

class OrderModel(models.Model):
    subtotal=models.IntegerField(default=0)
    shipping=models.IntegerField(default=0)
    grandtotal=models.IntegerField(default=0)
    customname=models.CharField(max_length=100,default='')
    customemail=models.CharField(max_length=100,default='')
    customaddress=models.CharField(max_length=100,default='')
    customphone=models.CharField(max_length=100,default='')
    paytype=models.CharField(max_length=50,default='')
    def __str__(self):
        return self.customname

class DetailModel(models.Model):
    dorder=models.ForeignKey('OrdersModel',on_delete=models.CASCADE)
    pname=models.CharField(max_length=100,default='')
    unitprice=models.IntegerField(default=0)
    quantity=models.IntegerField(default=0)
    dtotal=models.IntegerField(default=0)
    def __str__(self):
        return self.pname