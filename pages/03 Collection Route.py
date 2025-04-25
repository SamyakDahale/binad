import streamlit as st
import folium
from streamlit_folium import st_folium
from firebase_init import ref
import openrouteservice
from math import radians, sin, cos, sqrt, atan2
import json

API_KEY = "5b3ce3597851110001cf6248146e1c60d652417a95922c67108e0086"
FILL_THRESHOLD = 60
RADIUS_KM = 10  # Search radius from starting point

# if "user_logged_in" not in st.session_state or not st.session_state["user_logged_in"]:
#     st.warning("Please login first.")
#     st.stop()

# Helper: Haversine distance
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in kilometers
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# Page
st.title("Admin - Generate Optimized Waste Collection Route")

# Session state
if "route" not in st.session_state:
    st.session_state.route = None
if "full_bins" not in st.session_state:
    st.session_state.full_bins = None
if "coords" not in st.session_state:
    st.session_state.coords = None
if "start_point" not in st.session_state:
    st.session_state.start_point = None

# Step 1: Select starting point
st.subheader("Step 1: Select Starting Point on Map")
start_map = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
start_map.add_child(folium.LatLngPopup())

start_data = st_folium(start_map, height=350, width=700)

if start_data and start_data.get("last_clicked"):
    latlon = start_data["last_clicked"]
    st.session_state.start_point = [latlon["lng"], latlon["lat"]]  # [lon, lat]

if st.session_state.start_point:
    st.success(f"Starting point: {st.session_state.start_point[::-1]}")

# Step 2: Generate route
st.subheader("Step 2: Generate Route")

bins_ref = ref.get()
if bins_ref and st.session_state.start_point:
    start_lat = st.session_state.start_point[1]
    start_lon = st.session_state.start_point[0]

    full_bins = {}
    coords = []

    for bin_id, bin_data in bins_ref.items():
        if bin_data['fill_percentage'] > FILL_THRESHOLD:
            lat = bin_data['location']['lat']
            lon = bin_data['location']['lon']
            distance = haversine_distance(start_lat, start_lon, lat, lon)

            if distance <= RADIUS_KM:
                full_bins[bin_id] = bin_data
                coords.append([lon, lat])

    if len(coords) < 1:
        st.warning(f"No bins over {FILL_THRESHOLD}% found within {RADIUS_KM} km.")
    else:
        st.success(f"{len(coords)} bin(s) found within {RADIUS_KM} km.")

        st.session_state.full_bins = full_bins
        st.session_state.coords = coords

        if st.button("Generate Optimized Route"):
            try:
                full_coords = [st.session_state.start_point] + coords

                client = openrouteservice.Client(key=API_KEY)
                route = client.directions(
                    coordinates=full_coords,
                    profile='driving-car',
                    format='geojson',
                    optimize_waypoints=True
                )
                st.session_state.route = route
                st.success("Route generated!")
            except Exception as e:
                st.error(f"Failed to generate route: {e}")
elif not st.session_state.start_point:
    st.warning("Please select a starting point.")
else:
    st.warning("No bins found in database.")

# Step 3: Show map
if st.session_state.route and st.session_state.coords and st.session_state.full_bins:
    m = folium.Map(location=st.session_state.start_point[::-1], zoom_start=12)
    folium.GeoJson(st.session_state.route, name="Route").add_to(m)

    folium.Marker(
        location=st.session_state.start_point[::-1],
        popup="Starting Point",
        icon=folium.Icon(color="blue", icon="flag")
    ).add_to(m)

    for bin_id, bin_data in st.session_state.full_bins.items():
        lat = bin_data['location']['lat']
        lon = bin_data['location']['lon']
        popup_text = (
            f"ID: {bin_id}<br>"
            f"Type: {bin_data['type']}<br>"
            f"Fill: {bin_data['fill_percentage']}%"
        )
        folium.Marker(
            location=[lat, lon],
            popup=popup_text,
            icon=folium.Icon(color="orange")
        ).add_to(m)

    st_folium(m, height=600, width=800)
