# Production deployment

1. Point the DNS A/AAAA record for `FUELNET_DOMAIN` at the server.
2. Copy `.env.example` to `.env`, set strong secrets and valid SMTP values, then run `docker compose up -d --build`.
3. Caddy obtains and renews the HTTPS certificate automatically after DNS is live.
4. Verify `https://$FUELNET_DOMAIN/actuator/health`; scrape `/actuator/prometheus` from Prometheus.
5. Load test only an approved environment: `k6 run -e BASE_URL=https://$FUELNET_DOMAIN performance/smoke-load.js`.

## Django migration

Back up both databases. Then export Django tables with `mysqldump`, transform users/ECU/predictions to the Flyway schema, import into a staging copy, compare source and target row counts and sample prediction records, and only then migrate production during a maintenance window. The source credentials and schema are intentionally never stored in this repository.
