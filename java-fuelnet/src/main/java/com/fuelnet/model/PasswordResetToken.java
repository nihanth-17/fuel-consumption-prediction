package com.fuelnet.model;
import jakarta.persistence.*;import java.time.*;
@Entity public class PasswordResetToken {
 @Id @GeneratedValue(strategy=GenerationType.IDENTITY) private Long id;
 @ManyToOne(optional=false) private AppUser user;
 @Column(nullable=false,unique=true,length=128) private String tokenHash;
 @Column(nullable=false) private Instant expiresAt; private Instant usedAt;
 public AppUser getUser(){return user;} public String getTokenHash(){return tokenHash;} public Instant getExpiresAt(){return expiresAt;} public Instant getUsedAt(){return usedAt;}
 public void setUser(AppUser x){user=x;} public void setTokenHash(String x){tokenHash=x;} public void setExpiresAt(Instant x){expiresAt=x;} public void setUsedAt(Instant x){usedAt=x;}
}
