from django.db import models
from django.contrib.auth.models import User

class ECUData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    vehicle_speed = models.FloatField()
    engine_rpm = models.FloatField()
    throttle_position = models.FloatField()
    engine_load = models.FloatField()
    maf = models.FloatField(default=25.0)  # Add default
    intake_air_temp = models.FloatField(default=35.0)  # Add default
    coolant_temp = models.FloatField(default=85.0)  # Add default
    fuel_rail_pressure = models.FloatField(default=350.0)  # Add default
    acceleration = models.FloatField()
    brake_pedal_status = models.BooleanField(default=False)  # Add default
    gear_position = models.IntegerField()
    
    # Prediction results
    predicted_fuel_consumption = models.FloatField(null=True, blank=True)
    fuel_consumption_category = models.CharField(max_length=20, null=True, blank=True)
    driving_profile = models.CharField(max_length=20, null=True, blank=True)
    confidence_score = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f"ECU Data {self.id} - {self.driving_profile}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    vehicle_model = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

class PredictionResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ecu_data = models.ForeignKey(ECUData, on_delete=models.CASCADE)
    prediction_date = models.DateTimeField(auto_now_add=True)
    graph_image = models.TextField()  # Store base64 encoded graph
    
    def __str__(self):
        return f"Prediction {self.id} - {self.user.username}"