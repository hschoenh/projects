# Architecture

## Logical flow

```text
Harvard Dataverse
  -> Cloudera Flow Management / NiFi
  -> Amazon S3 raw zone
  -> Cloudera Data Warehouse / Impala
  -> Cloudera AI / Spark
  -> Streamlit dashboard
  -> optional predictive model
```

## Data locations

```text
Flights:
s3a://user036-buk-41effbce/data/user/user036/flight-demo/raw/flights/2008.csv

Carriers:
s3a://user036-buk-41effbce/data/user/user036/flight-demo/raw/carriers/carriers.csv

Airports:
s3a://user036-buk-41effbce/data/user/user036/flight-demo/raw/airports/airports.csv
```

## Design rationale

- NiFi handles ingestion and file movement.
- S3 is the shared durable data layer.
- Impala provides interactive SQL analytics.
- Spark in Cloudera AI reuses the same governed data for scalable analysis and ML.
- The dashboard consumes small aggregated outputs rather than rescanning the raw file on every page refresh.
