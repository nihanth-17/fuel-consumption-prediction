CREATE TABLE app_users (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  email VARCHAR(255), phone_number VARCHAR(50), vehicle_model VARCHAR(100), license_plate VARCHAR(20),
  role VARCHAR(20) NOT NULL DEFAULT 'USER', created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE ecu_data (
  id BIGINT AUTO_INCREMENT PRIMARY KEY, timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  vehicle_speed DOUBLE NOT NULL, engine_rpm DOUBLE NOT NULL, throttle_position DOUBLE NOT NULL, engine_load DOUBLE NOT NULL,
  maf DOUBLE NOT NULL, intake_air_temp DOUBLE NOT NULL, coolant_temp DOUBLE NOT NULL, fuel_rail_pressure DOUBLE NOT NULL,
  acceleration DOUBLE NOT NULL, brake_pedal_status BOOLEAN NOT NULL DEFAULT FALSE, gear_position INT NOT NULL,
  predicted_fuel_consumption DOUBLE NOT NULL, confidence_score DOUBLE NOT NULL,
  fuel_consumption_category VARCHAR(20), driving_profile VARCHAR(20)
);
CREATE TABLE prediction_result (
  id BIGINT AUTO_INCREMENT PRIMARY KEY, user_id BIGINT NOT NULL, ecu_data_id BIGINT NOT NULL UNIQUE,
  prediction_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_prediction_user FOREIGN KEY (user_id) REFERENCES app_users(id),
  CONSTRAINT fk_prediction_ecu FOREIGN KEY (ecu_data_id) REFERENCES ecu_data(id)
);
