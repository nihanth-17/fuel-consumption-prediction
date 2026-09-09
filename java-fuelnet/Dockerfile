FROM eclipse-temurin:21-jre
WORKDIR /app
COPY target/fuelnet-1.0.0.jar app.jar
RUN addgroup --system fuelnet && adduser --system --ingroup fuelnet fuelnet
USER fuelnet
EXPOSE 8080
ENTRYPOINT ["java","-XX:MaxRAMPercentage=75","-jar","/app/app.jar"]
