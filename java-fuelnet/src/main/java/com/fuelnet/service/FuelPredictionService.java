package com.fuelnet.service;

import org.springframework.stereotype.Service;
import java.util.*;

@Service
public class FuelPredictionService {
  public record Input(double vehicleSpeed, double engineRpm, double throttlePosition, double engineLoad, double maf, double intakeAirTemp, double acceleration, int gearPosition) {}
  public record Output(double fuelConsumption, String fuelCategory, String categoryColor, String drivingProfile, Map<String, Double> profileScores) {}

  public Output predict(Input x) {
    double fuel = estimateFuelLph(x);
    Map<String, Double> scores = scores(x);
    String profile = scores.entrySet().stream().max(Map.Entry.comparingByValue()).orElseThrow().getKey();
    String category = fuel < 4 ? "Very Low" : fuel < 6.5 ? "Low" : fuel < 9 ? "Medium" : fuel < 12 ? "High" : "Very High";
    String color = Map.of("Very Low", "#059669", "Low", "#10B981", "Medium", "#F59E0B", "High", "#EF4444", "Very High", "#DC2626").get(category);
    return new Output(fuel, category, color, profile, scores);
  }
  public double estimateFuelLph(Input x) {
    double t=clip(x.throttlePosition()/100,0,1), l=clip(x.engineLoad()/100,0,1), r=clip(x.engineRpm()/7000,0,1), s=clip(x.vehicleSpeed()/200,0,1), a=clip(Math.abs(x.acceleration())/5,0,1); int g=(int)clip(x.gearPosition(),1,6);
    return round(clip(1.5 + (t*.30+l*.25+r*.20+s*.15+a*.07+(1-g/6.0)*.03)*13.5, 1.5, 15));
  }
  public Map<String,Double> scores(Input x) {
    double s=x.vehicleSpeed(), r=x.engineRpm(), t=x.throttlePosition(), a=x.acceleration(); int g=x.gearPosition(); Map<String,Double> m=new LinkedHashMap<>();
    m.put("Aggressive",round(Math.min(100,t/100*35+Math.min(r,7000)/7000*25+Math.min(Math.max(a,0),5)/5*25+Math.max(0,4-g)/3.0*15)));
    m.put("Eco-Friendly",round(Math.min(100,Math.max(0,100-t)/100*35+Math.max(0,3000-r)/3000*25+Math.max(0,2-Math.abs(a))/2*25+Math.min(g,6)/6.0*15)));
    m.put("City",round(Math.min(100,Math.max(0,70-s)/70*40+Math.min(Math.abs(a),3)/3*30+Math.max(0,4-g)/3.0*30)));
    m.put("Highway",round(Math.min(100,Math.min(Math.max(s-60,0),120)/120*40+Math.min(g,6)/6.0*30+Math.max(0,80-t)/80*20+Math.max(0,1.5-Math.abs(a))/1.5*10)));
    m.put("Moderate",round(Math.min(100,Math.max(0,50-Math.abs(t-45))/50*30+Math.max(0,50-Math.abs((r-2500)/45))/50*25+Math.max(0,50-Math.abs(s-65))/50*25+Math.max(0,1-Math.abs(a))*20)));
    return m;
  }
  private double clip(double v,double lo,double hi){ return Math.max(lo,Math.min(hi,v)); }
  private double round(double v){ return Math.round(v*100.0)/100.0; }
}
