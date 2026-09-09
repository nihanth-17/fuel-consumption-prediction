import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def create_ecu_dataset():
    np.random.seed(42)
    n_samples = 10000
    
    # Generate realistic ECU data matching our model
    data = {
        'timestamp': [],
        'vehicle_speed_kmh': [],
        'engine_rpm': [],
        'throttle_position_percent': [],
        'engine_load_percent': [],
        'maf_gs': [],
        'intake_air_temp_c': [],
        'coolant_temp_c': [],
        'fuel_rail_pressure_kpa': [],
        'ambient_temp_c': [],
        'acceleration_ms2': [],
        'brake_pedal_status': [],
        'gear_position': [],
        'fuel_consumption_lph': [],
        'driving_profile': []
    }
    
    profiles = ['Aggressive', 'Moderate', 'Eco-Friendly', 'City', 'Highway']
    
    for i in range(n_samples):
        base_time = datetime(2024, 1, 1) + timedelta(seconds=i*10)
        data['timestamp'].append(base_time)
        
        profile = random.choice(profiles)
        
        if profile == 'Aggressive':
            speed = np.random.normal(80, 25)
            rpm = np.random.normal(3500, 800)
            throttle = np.random.normal(65, 20)
            acceleration = np.random.normal(2.5, 1.0)
        elif profile == 'Eco-Friendly':
            speed = np.random.normal(60, 15)
            rpm = np.random.normal(2200, 400)
            throttle = np.random.normal(35, 10)
            acceleration = np.random.normal(1.0, 0.5)
        elif profile == 'Highway':
            speed = np.random.normal(100, 10)
            rpm = np.random.normal(2800, 300)
            throttle = np.random.normal(45, 8)
            acceleration = np.random.normal(0.5, 0.3)
        elif profile == 'City':
            speed = np.random.normal(40, 20)
            rpm = np.random.normal(1800, 600)
            throttle = np.random.normal(30, 15)
            acceleration = np.random.normal(1.5, 1.2)
        else:  # Moderate
            speed = np.random.normal(70, 18)
            rpm = np.random.normal(2500, 500)
            throttle = np.random.normal(50, 12)
            acceleration = np.random.normal(1.2, 0.8)
        
        # Ensure realistic bounds
        speed = max(0, min(180, speed))
        rpm = max(600, min(7000, rpm))
        throttle = max(0, min(100, throttle))
        acceleration = max(-3, min(5, acceleration))
        
        # Calculate dependent parameters
        engine_load = min(100, (rpm * throttle) / 3500)
        maf = (rpm * throttle * engine_load) / 10000 + np.random.normal(0, 5)
        intake_temp = np.random.normal(35, 10)
        coolant_temp = min(110, max(70, intake_temp + 45 + np.random.normal(0, 3)))
        fuel_pressure = np.random.normal(350, 50)
        fuel_consumption = (maf * rpm * abs(acceleration+1) * throttle) / 50000 + np.random.normal(0, 0.2)
        
        # Add profile-specific fuel consumption patterns
        if profile == 'Aggressive':
            fuel_consumption *= 1.4
        elif profile == 'Eco-Friendly':
            fuel_consumption *= 0.7
        
        data['vehicle_speed_kmh'].append(round(speed, 2))
        data['engine_rpm'].append(int(rpm))
        data['throttle_position_percent'].append(round(throttle, 2))
        data['engine_load_percent'].append(round(engine_load, 2))
        data['maf_gs'].append(round(max(1, maf), 2))
        data['intake_air_temp_c'].append(round(intake_temp, 2))
        data['coolant_temp_c'].append(round(coolant_temp, 2))
        data['fuel_rail_pressure_kpa'].append(round(fuel_pressure, 2))
        data['ambient_temp_c'].append(np.random.normal(25, 15))
        data['acceleration_ms2'].append(round(acceleration, 2))
        data['brake_pedal_status'].append(random.choice([0, 1]))
        data['gear_position'].append(random.randint(1, 6))
        data['fuel_consumption_lph'].append(round(max(0.5, fuel_consumption), 2))
        data['driving_profile'].append(profile)
    
    df = pd.DataFrame(data)
    df.to_csv('dataset/ecu_fuel_consumption_data.csv', index=False)
    print(f"Dataset created with {n_samples} samples")
    print(df.head())
    print(f"\nDriving Profile Distribution:\n{df['driving_profile'].value_counts()}")

if __name__ == "__main__":
    create_ecu_dataset()