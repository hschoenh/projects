# Exercise Notes

## Scope

### Task 2B
Use NiFi / Flow Management to ingest historical airline data into S3.

### Task 3C
Use Cloudera Data Warehouse to answer:
1. Airport with most departures
2. Total flights per carrier
3. Carrier with worst punctuality

### Option B
Use Cloudera AI and Spark DataFrames to answer the same questions and optionally build a predictive model.

## KPI definition

```text
Delayed flight = arrival delay >= 15 minutes
```

Cancelled and diverted flights are excluded.

## Observed results

```text
ATL | William B Hartsfield-Atlanta Intl | 134,189 departures
WN  | Southwest Airlines Co.            | 398,966 flights
AA  | American Airlines Inc.            | 32.37% delayed
```
