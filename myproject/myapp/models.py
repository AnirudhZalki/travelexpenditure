from django.db import models

class VehicleTrip(models.Model):
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    distance = models.FloatField()
    tolls = models.IntegerField()
    fuel_cost = models.FloatField()
    toll_charges = models.FloatField()
    total = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.source} → {self.destination} ({self.total}₹)"
# Create your models here.

class Journey(models.Model):
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    distance_km = models.FloatField()
    toll_gates = models.IntegerField()
    fuel_cost = models.FloatField()
    toll_cost = models.FloatField()
    total_cost = models.FloatField()
    journey_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.source} to {self.destination} on {self.journey_date.strftime('%Y-%m-%d')}"