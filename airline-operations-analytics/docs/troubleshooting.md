# Troubleshooting

## NiFi PutHDFS

If PutHDFS reports:

```text
Could not find any Hadoop Configuration Resources on the classpath
```

Use:

```text
/etc/hadoop/conf.cloudera.stub_dfs/core-site.xml,
/etc/alternatives/hive-conf/hive-site.xml
```

Use path-only directories:

```text
/data/user/user036/flight-demo/raw/<subdir>
```

## NiFi scheduling

Source `InvokeHTTP`:

```text
Execution = Primary Node
```

Downstream processors with incoming connections:

```text
Execution = All Nodes
```

## Ranger / RAZ

`403 Ranger result: DENIED` indicates an authorization failure.

`400 Bad Request` and `404 NoSuchBucket` are separate issues and should not be treated as Ranger denials.

Verified exercise bucket:

```text
user036-buk-41effbce
```

## CDW executor startup

If Impala reports:

```text
Admission result: Queued
Waiting for executors to start
```

the Virtual Warehouse may be resuming from auto-suspend or waiting for executor capacity.

For demo stability, one option is:

```text
Auto-suspend timeout = 3600 seconds
```

## CAI session timeout

A timed-out development session does not delete project files. Start a new session and reconnect to Spark.

## Streamlit pattern

Recommended demo pattern:

```text
Spark session
 -> aggregate results
 -> export small result files
 -> Streamlit reads result files
```
