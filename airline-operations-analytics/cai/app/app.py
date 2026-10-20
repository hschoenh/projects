import streamlit as st
import pandas as pd

st.set_page_config(page_title="Airline Operations Analytics", layout="wide")

st.title("Airline Operations Analytics")
st.caption("Historical flight analytics powered by Cloudera AI and Apache Spark")

top_airports = pd.read_csv("top_airports.csv")
carrier_volume = pd.read_csv("carrier_volume.csv")
carrier_delay = pd.read_csv("carrier_delay.csv")

top_airport = top_airports.iloc[0]
top_carrier = carrier_volume.iloc[0]
worst_carrier = carrier_delay.iloc[0]

st.subheader("Operational Overview")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="Busiest Departure Airport",
        value=top_airport["airport_code"],
        delta=f'{int(top_airport["departures"]):,} departures'
    )
    st.caption(top_airport["airport_name"])
    st.markdown("#### Top 5 Airports")
    airport_top5 = top_airports.head(5)[["airport_code", "airport_name", "departures"]].copy()
    airport_top5.columns = ["Airport", "Airport Name", "Departures"]
    st.dataframe(airport_top5, use_container_width=True, hide_index=True)

with col2:
    st.metric(
        label="Highest Flight Volume",
        value=top_carrier["carrier_code"],
        delta=f'{int(top_carrier["total_flights"]):,} flights'
    )
    st.caption(top_carrier["carrier_name"])
    st.markdown("#### Top 5 Carriers")
    carrier_top5 = carrier_volume.head(5)[["carrier_code", "carrier_name", "total_flights"]].copy()
    carrier_top5.columns = ["Carrier", "Carrier Name", "Total Flights"]
    st.dataframe(carrier_top5, use_container_width=True, hide_index=True)

st.divider()

st.subheader("On-Time Performance")

st.metric(
    label="Worst On-Time Performance",
    value=worst_carrier["carrier_code"],
    delta=f'{worst_carrier["delay_rate_pct"]}% delayed'
)

st.caption(
    f'{worst_carrier["carrier_name"]} · '
    f'{int(worst_carrier["delayed_flights"]):,} delayed flights '
    f'out of {int(worst_carrier["evaluated_flights"]):,} evaluated'
)

st.markdown("#### Bottom 5 Carriers by On-Time Performance")

delay_top5 = carrier_delay.head(5)[
    ["carrier_code", "carrier_name", "evaluated_flights", "delayed_flights", "delay_rate_pct"]
].copy()

delay_top5.columns = ["Carrier", "Carrier Name", "Evaluated", "Delayed", "Delay Rate %"]
st.dataframe(delay_top5, use_container_width=True, hide_index=True)
