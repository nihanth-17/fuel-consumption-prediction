package com.fuelnet.model;
import jakarta.persistence.*;
import java.time.Instant;

@Entity
public class EcuData {
 @Id @GeneratedValue(strategy=GenerationType.IDENTITY) private Long id;
 private Instant timestamp=Instant.now();
 private double vehicleSpeed,engineRpm,throttlePosition,engineLoad,maf,intakeAirTemp,coolantTemp,fuelRailPressure,acceleration;
 private boolean brakePedalStatus; private int gearPosition; private double predictedFuelConsumption,confidenceScore;
 private String fuelConsumptionCategory,drivingProfile;
 public Long getId(){return id;} public Instant getTimestamp(){return timestamp;} public double getVehicleSpeed(){return vehicleSpeed;} public double getEngineRpm(){return engineRpm;} public double getThrottlePosition(){return throttlePosition;} public double getEngineLoad(){return engineLoad;} public double getMaf(){return maf;} public double getIntakeAirTemp(){return intakeAirTemp;} public double getAcceleration(){return acceleration;} public int getGearPosition(){return gearPosition;} public double getPredictedFuelConsumption(){return predictedFuelConsumption;} public String getFuelConsumptionCategory(){return fuelConsumptionCategory;} public String getDrivingProfile(){return drivingProfile;}
 public void setVehicleSpeed(double v){vehicleSpeed=v;} public void setEngineRpm(double v){engineRpm=v;} public void setThrottlePosition(double v){throttlePosition=v;} public void setEngineLoad(double v){engineLoad=v;} public void setMaf(double v){maf=v;} public void setIntakeAirTemp(double v){intakeAirTemp=v;} public void setCoolantTemp(double v){coolantTemp=v;} public void setFuelRailPressure(double v){fuelRailPressure=v;} public void setAcceleration(double v){acceleration=v;} public void setGearPosition(int v){gearPosition=v;} public void setPredictedFuelConsumption(double v){predictedFuelConsumption=v;} public void setFuelConsumptionCategory(String v){fuelConsumptionCategory=v;} public void setDrivingProfile(String v){drivingProfile=v;} public void setConfidenceScore(double v){confidenceScore=v;}
}
