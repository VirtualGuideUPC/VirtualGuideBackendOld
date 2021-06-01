from django.db import models

# Create your models here.

class TypePlace(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=255)

class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

class Province(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    department = models.ForeignKey(Department, null=False, blank=False, default="1", on_delete=models.CASCADE)

class TouristicPlace(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    cost_info = models.CharField(max_length=255)
    price = models.FloatField()
    schedule_info = models.CharField(max_length=255)
    historic_info = models.CharField(max_length=255)
    long_info = models.CharField(max_length=255)
    short_info = models.CharField(max_length=255)
    activities_info = models.CharField(max_length=255)
    latitude = models.CharField(max_length=16)
    longitude = models.CharField(max_length=16)
    range = models.IntegerField()
    province = models.ForeignKey(Province, null=False, blank=False, default="1", on_delete=models.CASCADE)
    type_place = models.ForeignKey(TypePlace, null=False, blank=False, default="1", on_delete=models.CASCADE)
    status = models.IntegerField(default=1)

class PictureTouristicPlace(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=255)
    number = models.IntegerField()
    touristic_place = models.ForeignKey(TouristicPlace, null=False, blank=False, default="1", on_delete=models.CASCADE)



