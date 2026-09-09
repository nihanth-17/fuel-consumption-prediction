package com.fuelnet.model;
import jakarta.persistence.*;
import java.time.Instant;
@Entity public class PredictionResult {
 @Id @GeneratedValue(strategy=GenerationType.IDENTITY) private Long id;
 @ManyToOne(optional=false) private AppUser user;
 @OneToOne(optional=false,cascade=CascadeType.ALL) private EcuData ecuData;
 private Instant predictionDate=Instant.now();
 public Long getId(){return id;} public AppUser getUser(){return user;} public EcuData getEcuData(){return ecuData;} public Instant getPredictionDate(){return predictionDate;}
 public void setUser(AppUser v){user=v;} public void setEcuData(EcuData v){ecuData=v;}
}
