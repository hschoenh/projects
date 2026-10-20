USE flight_demo;

CREATE EXTERNAL TABLE IF NOT EXISTS flight_demo.flights (
  year STRING,
  month STRING,
  dayofmonth STRING,
  dayofweek STRING,
  deptime STRING,
  crsdeptime STRING,
  arrtime STRING,
  crsarrtime STRING,
  uniquecarrier STRING,
  flightnum STRING,
  tailnum STRING,
  actualelapsedtime STRING,
  crselapsedtime STRING,
  airtime STRING,
  arrdelay STRING,
  depdelay STRING,
  origin STRING,
  dest STRING,
  distance STRING,
  taxiin STRING,
  taxiout STRING,
  cancelled STRING,
  cancellationcode STRING,
  diverted STRING,
  carrierdelay STRING,
  weatherdelay STRING,
  nasdelay STRING,
  securitydelay STRING,
  lateaircraftdelay STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION 's3a://user036-buk-41effbce/data/user/user036/flight-demo/raw/flights'
TBLPROPERTIES ('skip.header.line.count'='1');

CREATE EXTERNAL TABLE IF NOT EXISTS flight_demo.carriers (
  code STRING,
  description STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION 's3a://user036-buk-41effbce/data/user/user036/flight-demo/raw/carriers'
TBLPROPERTIES ('skip.header.line.count'='1');

CREATE EXTERNAL TABLE IF NOT EXISTS flight_demo.airports (
  iata STRING,
  airport STRING,
  city STRING,
  state STRING,
  country STRING,
  lat STRING,
  `long` STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION 's3a://user036-buk-41effbce/data/user/user036/flight-demo/raw/airports'
TBLPROPERTIES ('skip.header.line.count'='1');
