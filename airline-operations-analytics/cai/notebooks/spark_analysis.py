import cml.data_v1 as cmldata
from pyspark.sql import functions as F

CONNECTION_NAME = "user036-aw-dl"
BASE_PATH = "s3a://user036-buk-41effbce/data/user/user036/flight-demo/raw"

conn = cmldata.get_connection(CONNECTION_NAME)
spark = conn.get_spark_session()

flights = spark.read.option("header", "true").csv(f"{BASE_PATH}/flights/2008.csv")
carriers = spark.read.option("header", "true").csv(f"{BASE_PATH}/carriers/carriers.csv")
airports = spark.read.option("header", "true").csv(f"{BASE_PATH}/airports/airports.csv")

departures = (
    flights
    .filter(F.col("Cancelled").cast("int") == 0)
    .groupBy("Origin")
    .agg(F.count("*").alias("departures"))
)

airport_departures = (
    departures
    .join(airports, departures["Origin"] == airports["iata"], "left")
    .select(
        F.col("Origin").alias("airport_code"),
        F.col("airport").alias("airport_name"),
        "departures"
    )
    .orderBy(F.desc("departures"))
)

carrier_counts_named = (
    flights
    .groupBy("UniqueCarrier")
    .agg(F.count("*").alias("total_flights"))
    .join(carriers, F.col("UniqueCarrier") == F.col("Code"), "left")
    .select(
        F.col("UniqueCarrier").alias("carrier_code"),
        F.col("Description").alias("carrier_name"),
        "total_flights"
    )
    .orderBy(F.desc("total_flights"))
)

valid_flights = (
    flights
    .withColumn("arr_delay_num", F.col("ArrDelay").cast("double"))
    .filter(
        (F.col("Cancelled").cast("int") == 0)
        & (F.col("Diverted").cast("int") == 0)
        & F.col("arr_delay_num").isNotNull()
    )
)

carrier_delay_named = (
    valid_flights
    .groupBy("UniqueCarrier")
    .agg(
        F.count("*").alias("evaluated_flights"),
        F.sum(F.when(F.col("arr_delay_num") >= 15, 1).otherwise(0)).alias("delayed_flights")
    )
    .withColumn(
        "delay_rate_pct",
        F.round(100.0 * F.col("delayed_flights") / F.col("evaluated_flights"), 2)
    )
    .join(carriers, F.col("UniqueCarrier") == F.col("Code"), "left")
    .select(
        F.col("UniqueCarrier").alias("carrier_code"),
        F.col("Description").alias("carrier_name"),
        "evaluated_flights",
        "delayed_flights",
        "delay_rate_pct"
    )
    .orderBy(F.desc("delay_rate_pct"))
)

airport_departures.show(10, truncate=False)
carrier_counts_named.show(20, truncate=False)
carrier_delay_named.show(20, truncate=False)

airport_departures.limit(10).toPandas().to_csv("top_airports.csv", index=False)
carrier_counts_named.toPandas().to_csv("carrier_volume.csv", index=False)
carrier_delay_named.toPandas().to_csv("carrier_delay.csv", index=False)
