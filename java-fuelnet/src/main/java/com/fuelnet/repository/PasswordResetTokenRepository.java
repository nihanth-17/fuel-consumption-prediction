package com.fuelnet.repository;
import com.fuelnet.model.PasswordResetToken;import org.springframework.data.jpa.repository.JpaRepository;import java.util.*;
public interface PasswordResetTokenRepository extends JpaRepository<PasswordResetToken,Long>{Optional<PasswordResetToken> findByTokenHash(String hash);}
