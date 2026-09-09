package com.fuelnet.repository;
import com.fuelnet.model.*;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;
public interface PredictionRepository extends JpaRepository<PredictionResult, Long> {
  List<PredictionResult> findByUserOrderByPredictionDateDesc(AppUser user);
  List<PredictionResult> findAllByOrderByPredictionDateDesc();
}
