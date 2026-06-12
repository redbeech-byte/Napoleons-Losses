from pathlib import Path
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium

# Page setup
st.set_page_config(
    page_title="Napoleon's Battle Losses",
    layout="wide"
)

st.title("French Losses in Napoleons Most Significant Battles")

# Load data
folder = Path(__file__).resolve().parent
csv_path = folder / "Napoleons Losses.csv"

df = pd.read_csv(csv_path)
df.columns = df.columns.str.strip()

# Sidebar controls
st.sidebar.header("Map controls")

min_year = int(df["year"].min())
max_year = int(df["year"].max())

year_range = st.sidebar.slider(
    "Select years",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

filtered = df[
    (df["year"] >= year_range[0]) &
    (df["year"] <= year_range[1])
].copy()

# Map centered over Europe
m = folium.Map(
    location=[49.5, 12],
    zoom_start=5,
    tiles="OpenStreetMap"
)

# Add battle markers
for _, row in filtered.iterrows():
    radius = max(3, row["french_losses"]**0.5 / 12)

    popup_text = f"""
    <b>{row['battle']}</b><br>
    Year: {row['year']}<br>
    French losses: {row['french_losses']:,}
    """

    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=radius,
        popup=popup_text,
        tooltip=f"{row['battle']} ({row['year']})",
        color="black",
        fill=True,
        fill_color="darkred",
        fill_opacity=0.65,
        weight=1
    ).add_to(m)

# Show map
st_folium(m, width=1100, height=650)


