USE flight_demo;

-- 1. Which airport had the most departures?
SELECT
  f.origin AS airport_code,
  REGEXP_REPLACE(a.airport, '"', '') AS airport_name,
  COUNT(*) AS departures
FROM flight_demo.flights f
LEFT JOIN flight_demo.airports a
  ON f.origin = REGEXP_REPLACE(a.iata, '"', '')
WHERE CAST(f.cancelled AS INT) = 0
GROUP BY
  f.origin,
  REGEXP_REPLACE(a.airport, '"', '')
ORDER BY departures DESC
LIMIT 10;

-- 2. Total number of flights per carrier
SELECT
  f.uniquecarrier AS carrier_code,
  REGEXP_REPLACE(c.description, '"', '') AS carrier_name,
  COUNT(*) AS total_flights
FROM flight_demo.flights f
LEFT JOIN flight_demo.carriers c
  ON f.uniquecarrier = REGEXP_REPLACE(c.code, '"', '')
GROUP BY
  f.uniquecarrier,
  REGEXP_REPLACE(c.description, '"', '')
ORDER BY total_flights DESC;

-- 3. Worst on-time performance
WITH flight_delays AS (
  SELECT
    uniquecarrier,
    CASE
      WHEN arrdelay REGEXP '^-?[0-9]+(\.[0-9]+)?$'
      THEN CAST(arrdelay AS DOUBLE)
      ELSE NULL
    END AS arrival_delay
  FROM flight_demo.flights
  WHERE CAST(cancelled AS INT) = 0
    AND CAST(diverted AS INT) = 0
)
SELECT
  f.uniquecarrier AS carrier_code,
  REGEXP_REPLACE(c.description, '"', '') AS carrier_name,
  COUNT(f.arrival_delay) AS evaluated_flights,
  SUM(CASE WHEN f.arrival_delay >= 15 THEN 1 ELSE 0 END) AS delayed_flights,
  ROUND(
    100.0 * SUM(CASE WHEN f.arrival_delay >= 15 THEN 1 ELSE 0 END)
    / COUNT(f.arrival_delay),
    2
  ) AS delay_rate_pct
FROM flight_delays f
LEFT JOIN flight_demo.carriers c
  ON f.uniquecarrier = REGEXP_REPLACE(c.code, '"', '')
WHERE f.arrival_delay IS NOT NULL
GROUP BY
  f.uniquecarrier,
  REGEXP_REPLACE(c.description, '"', '')
ORDER BY delay_rate_pct DESC;
