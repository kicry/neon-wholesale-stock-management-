from django.db import models
from django.utils import timezone

# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True, serialize=False, auto_created=True)
    name=models.CharField(max_length=350)
    size = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    totalquantity = models.IntegerField(default=0)
    status = models.CharField(max_length=2, choices=(('1','Active'),('2','Inactive')), default=1)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Tempitem(models.Model):
    id = models.AutoField(primary_key=True, serialize=False, auto_created=True)
    tempname=models.CharField(max_length=350,blank=True, null=True)
    tempsize = models.CharField(max_length=50)
    tempprice = models.FloatField(default=0)
    tempquntity = models.IntegerField(default=0)
    temptotal = models.FloatField(default=0)

    def __str__(self):
        return self.tempname
    
class CustomerBill(models.Model):
    id = models.AutoField(primary_key=True, serialize=False, auto_created=True)
    custname = models.CharField(max_length=350)
    custnumb = models.IntegerField(default = 0 ,null=True, blank=True)
    custemail = models.EmailField(null=True, blank=True)
    totalitem = models.IntegerField(default = 0)
    totalprice = models.IntegerField(default = 0)
    discount = models.IntegerField(default = 0)
    per_discount = models.IntegerField(default = 0)
    payprice = models.IntegerField(default = 0)
    itemcode = models.CharField(max_length=50)
    payment = models.CharField(max_length=2, choices=(('1','Cash'),('2','Online'),('3','Pending')), default=1)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.custname + "-" + str(self.itemcode)


class invoiceitem(models.Model):
    id = models.AutoField(primary_key=True, serialize=False, auto_created=True)
    itemname = models.CharField(max_length=350,blank=True, null=True)
    itemsize = models.CharField(max_length=50)
    itemprice = models.FloatField(default=0)
    itemquntity = models.IntegerField(default=0)
    itemtotal = models.FloatField(default=0)
    itemcode = models.CharField(max_length=50)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.itemcode)

class stockhistory(models.Model):
    id = models.AutoField(primary_key=True, serialize=False, auto_created=True)
    itemname = models.CharField(max_length=350,blank=True, null=True)
    itemsize = models.CharField(max_length=50)
    itemquntity = models.IntegerField(default=0)
    status = models.CharField(max_length=2, choices=(('1','Stock in'),('2','Stock out')), default=1)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.itemname
