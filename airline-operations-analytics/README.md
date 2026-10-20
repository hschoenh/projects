# Airline Operations Analytics

This repository contains an end-to-end implementation covering:

- **Data Ingestion** – Historical flight data ingestion with Cloudera Flow Management / Apache NiFi
- **SQL Analytics** – SQL analytics with Cloudera Data Warehouse / Impala
- **Cloudera AI Analytics** – Spark-based analysis in Cloudera AI, including an interactive dashboard and an optional predictive model

## Business questions

1. Which airport had the most departures?
2. How many flights did each carrier operate?
3. Which carrier had the worst on-time performance?

For on-time performance, a delayed flight is defined as an **arrival at least 15 minutes late**. Cancelled and diverted flights are excluded.

## Architecture

```text
Harvard Dataverse
      |
      v
Cloudera Flow Management / NiFi
      |
      v
Amazon S3
      |
      +--------------------+
      |                    |
      v                    v
Cloudera Data Warehouse    Cloudera AI
Impala SQL                 Spark / PySpark
      |                    |
      v                    v
SQL insights          Aggregations / ML
                           |
                           v
                    Streamlit dashboard
```

## Repository structure

```text
.
├── README.md
├── docs/
│   ├── architecture.md
│   ├── implementation-notes.md
│   └── troubleshooting.md
├── nifi/
│   ├── README.md
│   └── flow-design.md
├── sql/
│   ├── 01_create_database.sql
│   ├── 02_create_external_tables.sql
│   └── 03_implementation_queries.sql
├── cai/
│   ├── notebooks/
│   │   └── spark_analysis.py
│   ├── app/
│   │   ├── app.py
│   │   └── requirements.txt
│   └── model/
│       └── delay_prediction.py
└── presentation/
    └── README.md
```

## Environment-specific values

```text
Environment: user036-cdp-env
Data Lake:   user036-aw-dl
S3 bucket:   user036-buk-41effbce
S3 base path:
s3a://user036-buk-41effbce/data/user/user036/flight-demo/raw
```

Do not commit credentials, passwords, tokens, or private customer information.

## NiFi ingestion

### Flight Ingest

```text
InvokeHTTP
  -> CompressContent (bzip2 decompress)
  -> UpdateAttribute (filename=2008.csv)
  -> PutHDFS
```

### Carrier Ingest

```text
InvokeHTTP
  -> UpdateAttribute (filename=carriers.csv)
  -> PutHDFS
```

### Airport Ingest

```text
InvokeHTTP
  -> UpdateAttribute (filename=airports.csv)
  -> PutHDFS
```

Working PutHDFS settings:

```text
Hadoop Configuration Resources:
/etc/hadoop/conf.cloudera.stub_dfs/core-site.xml,
/etc/alternatives/hive-conf/hive-site.xml

Kerberos User Service:
KerberosPasswordUserService

Directory:
/data/user/user036/flight-demo/raw/<subdir>

Conflict Resolution Strategy:
replace

Writing Strategy:
Simple write
```

## SQL analytics

Run:

```text
sql/01_create_database.sql
sql/02_create_external_tables.sql
sql/03_implementation_queries.sql
```

Observed results:

- **Busiest departure airport:** ATL – William B Hartsfield-Atlanta Intl – **134,189 departures**
- **Highest flight volume:** WN – Southwest Airlines Co. – **398,966 flights**
- **Worst on-time performance:** AA – American Airlines Inc. – **32.37% delayed**

## Cloudera AI

The Cloudera AI implementation:

1. Connects to the Spark Data Lake connection
2. Loads flights, carriers, and airports from S3
3. Recomputes the three business questions with PySpark
4. Exports small result sets for dashboard consumption
5. Serves them through Streamlit
6. Includes an optional Spark ML delay prediction pipeline

### Start dashboard

```bash
pip install -r cai/app/requirements.txt

streamlit run cai/app/app.py \
  --server.address 127.0.0.1 \
  --server.port $CDSW_APP_PORT \
  --server.headless true
```

## Predictive model

Target:

```text
Delayed = ArrDelay >= 15 minutes
```

Features:

- Month
- DayOfWeek
- CRSDepTime
- CRSArrTime
- UniqueCarrier
- Origin
- Dest
- Distance

The model intentionally avoids leakage from fields such as `ArrDelay`, `DepDelay`, `CarrierDelay`, and `LateAircraftDelay`.

## Scope note

This repository is intended for demonstration and learning purposes and is not a production deployment blueprint.
