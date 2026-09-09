# FuelNet Java conversion

This directory is the Java/Spring Boot port of the Django project. It contains the Spring Boot setup, JPA equivalents of `UserProfile`, `ECUData`, and `PredictionResult`, a REST backend, and a simple web UI.

## Run

1. Install JDK 17 and Maven.
2. Create a MySQL database/user matching `src/main/resources/application.properties` (or change those settings).
3. From this directory run `mvn spring-boot:run`, then open `http://localhost:8080`.

The original HTML files use Django template tags and therefore cannot run in Spring Boot. They are replaced here by `src/main/resources/static/index.html`.

The Java prediction service preserves the Python fallback calculation, fuel categories, and driving-profile scoring. The original scikit-learn Random Forest artifact is not portable to Java; integrating a Java ML library or exporting the trained model to ONNX is the next step if a trained Random Forest is required instead of this deterministic model.

## Python-to-Java mapping

| Python | Java target |
|---|---|
| `manage.py`, `FuelNet/settings.py` | `pom.xml`, `FuelNetApplication`, `application.properties` |
| `fuelapp/models.py` | `model/` JPA entities |
| `fuelapp/views.py` | Spring `@RestController` and prediction service |
| `dataset_creator.py`, `test_dataset_creator.py` | Java command-line utilities |
