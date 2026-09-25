import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import pandas as pd, numpy as np, streamlit as st, plotly.express as px
from src.twin.engine import DigitalTwin

st.set_page_config(page_title="India Climate Digital Twin",layout="wide")
st.title("🇮🇳 AI-Powered Digital Twin of India's Climate")
st.caption("Rainfall + temperature PoC using a national-data-ready pipeline")

df=pd.read_csv("data/sample/pilot_climate.csv",parse_dates=["date"])
states=sorted(df["region"].unique())
region=st.sidebar.selectbox("Pilot region",states)
temp_delta=st.sidebar.slider("What-if temperature change (°C)",-5.0,5.0,0.0,0.5)
rain_pct=st.sidebar.slider("What-if rainfall change (%)",-50,50,0,5)

g=df[df.region==region].copy()
latest=g.sort_values("date").tail(3)
hist=latest[["rainfall_mm","tmax_c","tmin_c"]].to_numpy()
twin=DigitalTwin()
pred=twin.predict(hist,temp_delta,rain_pct)

c1,c2,c3=st.columns(3)
c1.metric("Next-day rainfall",f"{pred[0]:.1f} mm")
c2.metric("Next-day max temp",f"{pred[1]:.1f} °C")
c3.metric("Scenario",f"{temp_delta:+.1f}°C / {rain_pct:+d}% rain")

st.subheader("Climate state")
fig=px.line(g,x="date",y=["rainfall_mm","tmax_c"],title=f"{region} history")
st.plotly_chart(fig,use_container_width=True)

st.subheader("Geospatial twin state")
latest_map=df.sort_values("date").groupby("region").tail(1)
fig2=px.scatter_geo(latest_map,lat="lat",lon="lon",color="rainfall_mm",
                    size="tmax_c",hover_name="region",
                    scope="asia",projection="natural earth",
                    title="Latest rainfall / temperature state")
st.plotly_chart(fig2,use_container_width=True)

st.subheader("What-if impact")
baseline=twin.predict(hist,0,0)
impact=pred-baseline
st.write({"rainfall_change_mm":float(impact[0]),"temperature_change_c":float(impact[1])})
st.info("Replace data/sample with authorized IMD/MOSDAC observations for research-grade results.")
