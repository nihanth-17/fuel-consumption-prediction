from django.contrib import admin
from .models import ECUData, UserProfile, PredictionResult

@admin.register(ECUData)
class ECUDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'vehicle_speed', 'engine_rpm', 'predicted_fuel_consumption', 'driving_profile', 'timestamp']
    list_filter = ['driving_profile', 'fuel_consumption_category', 'timestamp']
    search_fields = ['driving_profile']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'vehicle_model', 'license_plate', 'created_at']
    search_fields = ['user__username', 'vehicle_model', 'license_plate']

@admin.register(PredictionResult)
class PredictionResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'ecu_data', 'prediction_date']
    list_filter = ['prediction_date']
    search_fields = ['user__username']