package com.fuelnet.config;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import org.springframework.context.annotation.*;
@Configuration public class OpenApiConfig {
 @Bean OpenAPI fuelNetApi(){return new OpenAPI().info(new Info().title("FuelNet API").version("1.0.0").description("ECU fuel prediction and driving-profile classification API."));}
}
