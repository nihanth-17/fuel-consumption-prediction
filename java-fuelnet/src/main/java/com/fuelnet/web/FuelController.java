package com.fuelnet.web;

import com.fuelnet.model.*;
import com.fuelnet.repository.*;
import com.fuelnet.service.*;
import jakarta.servlet.http.HttpSession;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import java.util.*;
import java.io.File;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.security.crypto.password.PasswordEncoder;

@RestController @RequestMapping("/api")
public class FuelController {
  private final FuelPredictionService predictor; private final RandomForestModelService ml; private final ChartService charts; private final PasswordResetService resets; private final UserRepository users; private final PredictionRepository predictions; private final PasswordEncoder passwords;
  public FuelController(FuelPredictionService p, RandomForestModelService m, ChartService c, PasswordResetService rs, UserRepository u, PredictionRepository r, PasswordEncoder pe){ predictor=p; ml=m; charts=c; resets=rs; users=u; predictions=r; passwords=pe; }
  @PostMapping("/register") public ResponseEntity<?> register(@RequestBody AppUser u) {
    if(u.getUsername()==null || u.getPassword()==null) return ResponseEntity.badRequest().body(Map.of("error","Username and password are required"));
    if(users.findByUsername(u.getUsername()).isPresent()) return ResponseEntity.badRequest().body(Map.of("error","Username already exists"));
    u.setPassword(passwords.encode(u.getPassword())); users.save(u); return ResponseEntity.status(201).body(Map.of("message","Registration successful"));
  }
  @PostMapping("/login") public ResponseEntity<?> login(@RequestBody Map<String,String> b,HttpSession s) {
    return users.findByUsername(b.get("username")).filter(u->passwords.matches(b.get("password"),u.getPassword())).<ResponseEntity<?>>map(u->{s.setAttribute("userId",u.getId()); return ResponseEntity.ok(Map.of("message","Logged in"));}).orElse(ResponseEntity.status(401).body(Map.of("error","Invalid username or password")));
  }
  @PostMapping("/admin/login") public ResponseEntity<?> admin(@RequestBody Map<String,String> b,HttpSession s) {
    return users.findByUsername(b.get("username")).filter(u->"ADMIN".equals(u.getRole()) && passwords.matches(b.get("password"),u.getPassword())).<ResponseEntity<?>>map(u->{s.setAttribute("admin",true);s.setAttribute("userId",u.getId());return ResponseEntity.ok(Map.of("message","Admin logged in"));}).orElse(ResponseEntity.status(401).body(Map.of("error","Invalid admin credentials")));
  }
  @PostMapping("/logout") public Map<String,String> logout(HttpSession s){s.invalidate();return Map.of("message","Logged out");}
  @PostMapping("/password-reset/request") public Map<String,String> requestReset(@RequestBody Map<String,String>b){resets.request(b.get("email"));return Map.of("message","If that account exists, a reset email was sent.");}
  @PostMapping("/password-reset/confirm") public Map<String,String> confirmReset(@RequestBody Map<String,String>b){resets.reset(b.get("token"),b.get("password"));return Map.of("message","Password reset complete.");}
  @PostMapping("/predict") public ResponseEntity<?> predict(@RequestBody FuelPredictionService.Input x,HttpSession s) {
    Object id=s.getAttribute("userId"); if(id==null)return ResponseEntity.status(401).body(Map.of("error","Login required"));
    FuelPredictionService.Output o=predictor.predict(x); try{var m=ml.predict(x);if(m.isPresent())o=new FuelPredictionService.Output(m.get().fuel(),o.fuelCategory(),o.categoryColor(),m.get().profile(),o.profileScores());}catch(Exception ignored){} EcuData e=new EcuData(); e.setVehicleSpeed(x.vehicleSpeed());e.setEngineRpm(x.engineRpm());e.setThrottlePosition(x.throttlePosition());e.setEngineLoad(x.engineLoad());e.setMaf(x.maf());e.setIntakeAirTemp(x.intakeAirTemp());e.setAcceleration(x.acceleration());e.setGearPosition(x.gearPosition());e.setCoolantTemp(Math.max(70,Math.min(100,x.intakeAirTemp()+50)));e.setFuelRailPressure(350);e.setPredictedFuelConsumption(o.fuelConsumption());e.setFuelConsumptionCategory(o.fuelCategory());e.setDrivingProfile(o.drivingProfile());e.setConfidenceScore(85);
    PredictionResult r=new PredictionResult();r.setUser(users.getReferenceById((Long)id));r.setEcuData(e);predictions.save(r);return ResponseEntity.ok(Map.of("prediction",o,"chartSvg",charts.profileChart(o.profileScores(),o.drivingProfile(),o.fuelConsumption())));
  }
  @GetMapping("/predictions") public ResponseEntity<?> mine(HttpSession s){Object id=s.getAttribute("userId");if(id==null)return ResponseEntity.status(401).build();return ResponseEntity.ok(predictions.findByUserOrderByPredictionDateDesc(users.getReferenceById((Long)id)));}
  @GetMapping("/admin/predictions") public ResponseEntity<?> all(HttpSession s){if(!Boolean.TRUE.equals(s.getAttribute("admin")))return ResponseEntity.status(403).build();return ResponseEntity.ok(predictions.findAllByOrderByPredictionDateDesc());}
  @PostMapping("/admin/train") public ResponseEntity<?> train(@RequestParam("dataset") MultipartFile f,HttpSession s) throws Exception {if(!Boolean.TRUE.equals(s.getAttribute("admin")))return ResponseEntity.status(403).build();if(f.isEmpty())return ResponseEntity.badRequest().body(Map.of("error","CSV required"));File tmp=File.createTempFile("fuelnet-",".csv");try{f.transferTo(tmp);return ResponseEntity.ok(ml.train(tmp));}finally{tmp.delete();}}
}
