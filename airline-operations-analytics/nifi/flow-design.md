# NiFi Flow Design

## Flight Ingest

```text
InvokeHTTP
 -> CompressContent
 -> UpdateAttribute
 -> PutHDFS
```

### InvokeHTTP

```text
Method: GET
URL:
https://dataverse.harvard.edu/api/access/datafile/:persistentId?persistentId=doi:10.7910/DVN/HG7NV7/EIR0RA

Execution:
Primary Node
```

### CompressContent

```text
Mode: decompress
Compression Format: bzip2
Update Filename: true
Execution: All Nodes
```

### UpdateAttribute

```text
filename = 2008.csv
```

### PutHDFS

```text
Hadoop Configuration Resources:
/etc/hadoop/conf.cloudera.stub_dfs/core-site.xml,
/etc/alternatives/hive-conf/hive-site.xml

Kerberos User Service:
KerberosPasswordUserService

Directory:
/data/user/user036/flight-demo/raw/flights

Conflict Resolution Strategy:
replace

Writing Strategy:
Simple write
```

## Carrier Ingest

```text
InvokeHTTP
 -> UpdateAttribute(filename=carriers.csv)
 -> PutHDFS(/data/user/user036/flight-demo/raw/carriers)
```

No bzip2 decompression is required.

## Airport Ingest

```text
InvokeHTTP
 -> UpdateAttribute(filename=airports.csv)
 -> PutHDFS(/data/user/user036/flight-demo/raw/airports)
```

No bzip2 decompression is required.
