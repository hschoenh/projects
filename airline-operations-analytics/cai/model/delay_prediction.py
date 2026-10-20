import cml.data_v1 as cmldata
from pyspark.sql import functions as F
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator

CONNECTION_NAME = "user036-aw-dl"
FLIGHTS_PATH = (
    "s3a://user036-buk-41effbce/"
    "data/user/user036/flight-demo/raw/flights/2008.csv"
)

conn = cmldata.get_connection(CONNECTION_NAME)
spark = conn.get_spark_session()

flights = spark.read.option("header", "true").csv(FLIGHTS_PATH)

ml_data = (
    flights
    .withColumn("label", F.when(F.col("ArrDelay").cast("double") >= 15, 1.0).otherwise(0.0))
    .filter(
        (F.col("Cancelled").cast("int") == 0)
        & (F.col("Diverted").cast("int") == 0)
        & F.col("ArrDelay").cast("double").isNotNull()
    )
    .withColumn("Month_num", F.col("Month").cast("double"))
    .withColumn("DayOfWeek_num", F.col("DayOfWeek").cast("double"))
    .withColumn("CRSDepTime_num", F.col("CRSDepTime").cast("double"))
    .withColumn("CRSArrTime_num", F.col("CRSArrTime").cast("double"))
    .withColumn("Distance_num", F.col("Distance").cast("double"))
    .dropna(subset=[
        "Month_num", "DayOfWeek_num", "CRSDepTime_num", "CRSArrTime_num",
        "Distance_num", "UniqueCarrier", "Origin", "Dest"
    ])
)

carrier_indexer = StringIndexer(inputCol="UniqueCarrier", outputCol="carrier_index", handleInvalid="keep")
origin_indexer = StringIndexer(inputCol="Origin", outputCol="origin_index", handleInvalid="keep")
dest_indexer = StringIndexer(inputCol="Dest", outputCol="dest_index", handleInvalid="keep")

encoder = OneHotEncoder(
    inputCols=["carrier_index", "origin_index", "dest_index"],
    outputCols=["carrier_vec", "origin_vec", "dest_vec"]
)

assembler = VectorAssembler(
    inputCols=[
        "Month_num", "DayOfWeek_num", "CRSDepTime_num", "CRSArrTime_num",
        "Distance_num", "carrier_vec", "origin_vec", "dest_vec"
    ],
    outputCol="features"
)

lr = LogisticRegression(featuresCol="features", labelCol="label", maxIter=20)

pipeline = Pipeline(stages=[
    carrier_indexer, origin_indexer, dest_indexer, encoder, assembler, lr
])

train_df, test_df = ml_data.randomSplit([0.8, 0.2], seed=42)

model = pipeline.fit(train_df)
predictions = model.transform(test_df)

evaluator = BinaryClassificationEvaluator(
    labelCol="label",
    rawPredictionCol="rawPrediction",
    metricName="areaUnderROC"
)

auc = evaluator.evaluate(predictions)
print("ROC-AUC:", round(auc, 4))

predictions.select(
    "UniqueCarrier", "Origin", "Dest", "label", "prediction", "probability"
).show(20, truncate=False)
