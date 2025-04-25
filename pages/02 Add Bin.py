import streamlit as st
from firebase_init import ref
from streamlit_folium import st_folium
import folium

st.title("Admin - Add New Dustbin")

# if "user_logged_in" not in st.session_state or not st.session_state["user_logged_in"]:
#     st.warning("Please login first.")
#     st.stop()

# Initial center point (e.g., India)
initial_location = [20.5937, 78.9629]
m = folium.Map(location=initial_location, zoom_start=5)

# Add click handler
m.add_child(folium.LatLngPopup())
 
st.write("Click on the map to select location")
map_data = st_folium(m, height=400, width=700)

# Retrieve lat/lon from click
lat = None
lon = None
if map_data and map_data["last_clicked"]:
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]
    st.success(f"Selected Location: Latitude = {lat:.6f}, Longitude = {lon:.6f}")

bin_type = st.selectbox("Select Bin Type", ["plastic", "paper", "glass",  "carboard", "trash", "metal"])
fill_percentage = st.slider("Fill Percentage", 0, 100, 50)

if st.button("Add Bin"):
    if lat is None or lon is None:
        st.error("Please select a location on the map first.")
    else:
        bin_id = ref.push().key  # Unique ID

        bin_data = {
            'location': {
                'lat': lat,
                'lon': lon
            },
            'type': bin_type,
            'fill_percentage': fill_percentage
        }

        ref.child(bin_id).set(bin_data)
        st.success(f"Bin added successfully with ID: {bin_id}")
