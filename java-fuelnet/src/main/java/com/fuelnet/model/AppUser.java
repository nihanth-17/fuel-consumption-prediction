package com.fuelnet.model;

import jakarta.persistence.*;
import java.time.Instant;

@Entity @Table(name = "app_users")
public class AppUser {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY) private Long id;
    @Column(unique = true, nullable = false) private String username;
    @Column(nullable = false) private String password; // Replace with BCrypt before production.
    private String email, phoneNumber, vehicleModel, licensePlate;
    @Column(nullable = false) private String role = "USER";
    private Instant createdAt = Instant.now();
    public Long getId() { return id; } public String getUsername() { return username; }
    public String getPassword() { return password; } public String getEmail() { return email; }
    public String getPhoneNumber() { return phoneNumber; } public String getVehicleModel() { return vehicleModel; }
    public String getLicensePlate() { return licensePlate; }
    public String getRole() { return role; }
    public void setUsername(String v) { username=v; } public void setPassword(String v) { password=v; }
    public void setEmail(String v) { email=v; } public void setPhoneNumber(String v) { phoneNumber=v; }
    public void setVehicleModel(String v) { vehicleModel=v; } public void setLicensePlate(String v) { licensePlate=v; }
    public void setRole(String v) { role=v; }
}
