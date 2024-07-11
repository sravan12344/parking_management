from django.db import models
from datetime import datetime

class Admin(models.Model):
    name = models.CharField(max_length=120, null=False, blank=False)
    username = models.CharField(max_length=100, null=False, blank=False)
    password = models.CharField(max_length=100, null=False, blank=False)  # added null=False, blank=False


class Category(models.Model):
    parking_Area_no = models.CharField(max_length=200, null=False)
    vehicle_type = models.CharField(max_length=200, null=False)
    vehicle_limit = models.CharField(max_length=100, null=False, blank=False)
    parking_charge = models.CharField(max_length=200, null=False)
    vehicle_count = models.IntegerField(default=0)
    status = models.BooleanField(null=False, default=True)  # changed null=True to null=False, added default=False
    doc = models.DateTimeField(auto_now_add=True)  # changed default=datetime.now to auto_now_add=True


class AddVehicle(models.Model):
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, blank=False)  # changed categories to category
    vehicle_no = models.CharField(max_length=200, null=False, blank=False)  # changed blank=True to blank=False
    status = models.BooleanField(null=False, default=True)  # changed null=True to null=False, added default=False
    arrival_time = models.DateTimeField(auto_now_add=True)  # changed default=datetime.now to auto_now_add=True




# Create your models here.
