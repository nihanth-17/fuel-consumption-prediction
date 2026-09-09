import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def calculate_efficiency_score(speed, rpm, throttle, acceleration, gear):
    """Calculate efficiency score based on input parameters"""
    efficiency_score = 0
    
    # Positive factors (lower consumption)
    if rpm < 2500:
        efficiency_score += 2
    if throttle < 40:
        efficiency_score += 2
    if speed >= 60 and speed <= 80:  # Most efficient speed range
        efficiency_score += 2
    if gear >= 5:  # Higher gears more efficient
        efficiency_score += 1
    if acceleration < 1.5:  # Smooth acceleration
        efficiency_score += 1
    
    # Negative factors (higher consumption)
    if rpm > 4000:
        efficiency_score -= 3
    if throttle > 70:
        efficiency_score -= 3
    if speed > 100:  # High speed increases consumption
        efficiency_score -= 2
    if acceleration > 2.5:  # Aggressive acceleration
        efficiency_score -= 2
    if gear <= 2:  # Low gears less efficient
        efficiency_score -= 1
    
    return efficiency_score

def get_fuel_category(efficiency_score):
    """Get fuel category based on efficiency score"""
    if efficiency_score >= 7:
        return "Very Low", "#059669"
    elif efficiency_score >= 5:
        return "Low", "#10B981"
    elif efficiency_score >= 3:
        return "Medium", "#F59E0B"
    elif efficiency_score >= 1:
        return "High", "#EF4444"
    else:
        return "Very High", "#DC2626"

def get_driving_profile(speed, rpm, throttle, acceleration, gear):
    """Get driving profile based on parameters"""
    if throttle > 70 or acceleration > 2.5 or rpm > 4000:
        return "Aggressive"
    elif throttle < 35 and acceleration < 1.0 and rpm < 2500:
        return "Eco-Friendly" 
    elif speed < 50 and gear <= 3:
        return "City"
    elif speed > 90 and gear >= 5:
        return "Highway"
    else:
        return "Moderate"

def create_test_dataset():
    # Create test data for different categories
    test_data = []
    
    # 🟢 VERY LOW Consumption (Efficiency Score 7-10) - 10 samples
    print("Creating VERY LOW consumption samples...")
    for i in range(10):
        speed = np.random.uniform(60, 75)
        rpm = np.random.uniform(1800, 2400)
        throttle = np.random.uniform(25, 38)
        acceleration = np.random.uniform(0.3, 1.2)
        gear = np.random.choice([5, 6])
        engine_load = np.random.uniform(40, 55)
        maf = np.random.uniform(15, 22)
        
        efficiency_score = calculate_efficiency_score(speed, rpm, throttle, acceleration, gear)
        fuel_category, color = get_fuel_category(efficiency_score)
        driving_profile = get_driving_profile(speed, rpm, throttle, acceleration, gear)
        
        # Calculate realistic fuel consumption
        fuel_consumption = (rpm * throttle * engine_load) / 60000
        fuel_consumption = max(1.5, min(3.0, fuel_consumption))
        
        test_data.append({
            'timestamp': datetime(2024, 1, 1) + timedelta(minutes=i*10),
            'vehicle_speed_kmh': round(speed, 2),
            'engine_rpm': int(rpm),
            'throttle_position_percent': round(throttle, 2),
            'engine_load_percent': round(engine_load, 2),
            'maf_gs': round(maf, 2),
            'intake_air_temp_c': round(np.random.uniform(25, 32), 2),
            'coolant_temp_c': round(np.random.uniform(75, 85), 2),
            'fuel_rail_pressure_kpa': round(np.random.uniform(320, 360), 2),
            'ambient_temp_c': round(np.random.uniform(20, 28), 2),
            'acceleration_ms2': round(acceleration, 2),
            'brake_pedal_status': np.random.choice([0, 1], p=[0.9, 0.1]),
            'gear_position': gear,
            'fuel_consumption_lph': round(fuel_consumption, 2),
            'driving_profile': driving_profile,
            'consumption_category': fuel_category,
            'efficiency_score': efficiency_score
        })
    
    # 🟡 LOW Consumption (Efficiency Score 5-6) - 10 samples
    print("Creating LOW consumption samples...")
    for i in range(10):
        speed = np.random.uniform(65, 85)
        rpm = np.random.uniform(2200, 2800)
        throttle = np.random.uniform(35, 50)
        acceleration = np.random.uniform(0.8, 1.8)
        gear = np.random.choice([4, 5, 6])
        engine_load = np.random.uniform(50, 65)
        maf = np.random.uniform(20, 30)
        
        efficiency_score = calculate_efficiency_score(speed, rpm, throttle, acceleration, gear)
        fuel_category, color = get_fuel_category(efficiency_score)
        driving_profile = get_driving_profile(speed, rpm, throttle, acceleration, gear)
        
        fuel_consumption = (rpm * throttle * engine_load) / 55000
        fuel_consumption = max(2.5, min(4.5, fuel_consumption))
        
        test_data.append({
            'timestamp': datetime(2024, 1, 1) + timedelta(minutes=(i+10)*10),
            'vehicle_speed_kmh': round(speed, 2),
            'engine_rpm': int(rpm),
            'throttle_position_percent': round(throttle, 2),
            'engine_load_percent': round(engine_load, 2),
            'maf_gs': round(maf, 2),
            'intake_air_temp_c': round(np.random.uniform(28, 36), 2),
            'coolant_temp_c': round(np.random.uniform(78, 88), 2),
            'fuel_rail_pressure_kpa': round(np.random.uniform(330, 370), 2),
            'ambient_temp_c': round(np.random.uniform(22, 30), 2),
            'acceleration_ms2': round(acceleration, 2),
            'brake_pedal_status': np.random.choice([0, 1], p=[0.8, 0.2]),
            'gear_position': gear,
            'fuel_consumption_lph': round(fuel_consumption, 2),
            'driving_profile': driving_profile,
            'consumption_category': fuel_category,
            'efficiency_score': efficiency_score
        })
    
    # 🟠 MEDIUM Consumption (Efficiency Score 3-4) - 10 samples
    print("Creating MEDIUM consumption samples...")
    for i in range(10):
        speed = np.random.uniform(70, 95)
        rpm = np.random.uniform(2600, 3500)
        throttle = np.random.uniform(45, 65)
        acceleration = np.random.uniform(1.2, 2.2)
        gear = np.random.choice([3, 4, 5])
        engine_load = np.random.uniform(60, 75)
        maf = np.random.uniform(25, 40)
        
        efficiency_score = calculate_efficiency_score(speed, rpm, throttle, acceleration, gear)
        fuel_category, color = get_fuel_category(efficiency_score)
        driving_profile = get_driving_profile(speed, rpm, throttle, acceleration, gear)
        
        fuel_consumption = (rpm * throttle * engine_load) / 50000
        fuel_consumption = max(4.0, min(6.5, fuel_consumption))
        
        test_data.append({
            'timestamp': datetime(2024, 1, 1) + timedelta(minutes=(i+20)*10),
            'vehicle_speed_kmh': round(speed, 2),
            'engine_rpm': int(rpm),
            'throttle_position_percent': round(throttle, 2),
            'engine_load_percent': round(engine_load, 2),
            'maf_gs': round(maf, 2),
            'intake_air_temp_c': round(np.random.uniform(30, 40), 2),
            'coolant_temp_c': round(np.random.uniform(80, 92), 2),
            'fuel_rail_pressure_kpa': round(np.random.uniform(340, 380), 2),
            'ambient_temp_c': round(np.random.uniform(25, 35), 2),
            'acceleration_ms2': round(acceleration, 2),
            'brake_pedal_status': np.random.choice([0, 1], p=[0.7, 0.3]),
            'gear_position': gear,
            'fuel_consumption_lph': round(fuel_consumption, 2),
            'driving_profile': driving_profile,
            'consumption_category': fuel_category,
            'efficiency_score': efficiency_score
        })
    
    # 🔴 HIGH Consumption (Efficiency Score 1-2) - 10 samples
    print("Creating HIGH consumption samples...")
    for i in range(10):
        speed = np.random.uniform(85, 110)
        rpm = np.random.uniform(3500, 4500)
        throttle = np.random.uniform(60, 80)
        acceleration = np.random.uniform(2.0, 3.0)
        gear = np.random.choice([2, 3, 4])
        engine_load = np.random.uniform(70, 85)
        maf = np.random.uniform(35, 55)
        
        efficiency_score = calculate_efficiency_score(speed, rpm, throttle, acceleration, gear)
        fuel_category, color = get_fuel_category(efficiency_score)
        driving_profile = get_driving_profile(speed, rpm, throttle, acceleration, gear)
        
        fuel_consumption = (rpm * throttle * engine_load) / 45000
        fuel_consumption = max(6.0, min(9.0, fuel_consumption))
        
        test_data.append({
            'timestamp': datetime(2024, 1, 1) + timedelta(minutes=(i+30)*10),
            'vehicle_speed_kmh': round(speed, 2),
            'engine_rpm': int(rpm),
            'throttle_position_percent': round(throttle, 2),
            'engine_load_percent': round(engine_load, 2),
            'maf_gs': round(maf, 2),
            'intake_air_temp_c': round(np.random.uniform(35, 45), 2),
            'coolant_temp_c': round(np.random.uniform(85, 98), 2),
            'fuel_rail_pressure_kpa': round(np.random.uniform(350, 400), 2),
            'ambient_temp_c': round(np.random.uniform(28, 38), 2),
            'acceleration_ms2': round(acceleration, 2),
            'brake_pedal_status': np.random.choice([0, 1], p=[0.6, 0.4]),
            'gear_position': gear,
            'fuel_consumption_lph': round(fuel_consumption, 2),
            'driving_profile': driving_profile,
            'consumption_category': fuel_category,
            'efficiency_score': efficiency_score
        })
    
    # 🚨 VERY HIGH Consumption (Efficiency Score <1) - 10 samples
    print("Creating VERY HIGH consumption samples...")
    for i in range(10):
        speed = np.random.uniform(100, 140)
        rpm = np.random.uniform(4500, 6000)
        throttle = np.random.uniform(75, 95)
        acceleration = np.random.uniform(2.5, 4.0)
        gear = np.random.choice([2, 3])
        engine_load = np.random.uniform(80, 95)
        maf = np.random.uniform(50, 75)
        
        efficiency_score = calculate_efficiency_score(speed, rpm, throttle, acceleration, gear)
        fuel_category, color = get_fuel_category(efficiency_score)
        driving_profile = get_driving_profile(speed, rpm, throttle, acceleration, gear)
        
        fuel_consumption = (rpm * throttle * engine_load) / 40000
        fuel_consumption = max(8.0, min(15.0, fuel_consumption))
        
        test_data.append({
            'timestamp': datetime(2024, 1, 1) + timedelta(minutes=(i+40)*10),
            'vehicle_speed_kmh': round(speed, 2),
            'engine_rpm': int(rpm),
            'throttle_position_percent': round(throttle, 2),
            'engine_load_percent': round(engine_load, 2),
            'maf_gs': round(maf, 2),
            'intake_air_temp_c': round(np.random.uniform(40, 50), 2),
            'coolant_temp_c': round(np.random.uniform(90, 105), 2),
            'fuel_rail_pressure_kpa': round(np.random.uniform(370, 420), 2),
            'ambient_temp_c': round(np.random.uniform(30, 40), 2),
            'acceleration_ms2': round(acceleration, 2),
            'brake_pedal_status': np.random.choice([0, 1], p=[0.5, 0.5]),
            'gear_position': gear,
            'fuel_consumption_lph': round(fuel_consumption, 2),
            'driving_profile': driving_profile,
            'consumption_category': fuel_category,
            'efficiency_score': efficiency_score
        })
    
    # Create DataFrame
    df = pd.DataFrame(test_data)
    
    # Save to CSV
    df.to_csv('dataset/test_dataset.csv', index=False)
    
    print("\n✅ Test dataset created successfully!")
    print(f"📊 Total samples: {len(df)}")
    
    # Display summary
    print("\n📈 Consumption Category Distribution:")
    category_summary = df['consumption_category'].value_counts().sort_index()
    for category, count in category_summary.items():
        print(f"   {category}: {count} samples")
    
    print("\n🚗 Driving Profile Distribution:")
    profile_summary = df['driving_profile'].value_counts()
    for profile, count in profile_summary.items():
        print(f"   {profile}: {count} samples")
    
    print("\n🎯 Efficiency Score Range:")
    print(f"   Min: {df['efficiency_score'].min()}")
    print(f"   Max: {df['efficiency_score'].max()}")
    print(f"   Avg: {df['efficiency_score'].mean():.1f}")
    
    print(f"\n📁 File saved as: dataset/test_dataset.csv")
    
    # Display sample from each category
    print("\n🔍 Sample from each consumption category:")
    categories = df['consumption_category'].unique()
    for category in categories:
        sample = df[df['consumption_category'] == category].iloc[0]
        print(f"\n{category}:")
        print(f"  Speed: {sample['vehicle_speed_kmh']} km/h")
        print(f"  RPM: {sample['engine_rpm']}")
        print(f"  Throttle: {sample['throttle_position_percent']}%")
        print(f"  Gear: {sample['gear_position']}")
        print(f"  Acceleration: {sample['acceleration_ms2']} m/s²")
        print(f"  Efficiency Score: {sample['efficiency_score']}")
        print(f"  Fuel: {sample['fuel_consumption_lph']} LPH")
        print(f"  Profile: {sample['driving_profile']}")

if __name__ == "__main__":
    create_test_dataset()