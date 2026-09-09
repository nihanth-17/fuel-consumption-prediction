package com.fuelnet;
import com.fuelnet.service.FuelPredictionService;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class FuelPredictionServiceTest {
 private final FuelPredictionService service = new FuelPredictionService();
 @Test void fuelIsBounded(){var o=service.predict(new FuelPredictionService.Input(200,7000,100,100,80,35,5,1));assertTrue(o.fuelConsumption() >= 1.5 && o.fuelConsumption() <= 15.0);}
 @Test void ecoInputHasEcoScore(){var o=service.predict(new FuelPredictionService.Input(65,2000,20,40,15,30,.2,6));assertTrue(o.profileScores().get("Eco-Friendly") > o.profileScores().get("Aggressive"));}
}
