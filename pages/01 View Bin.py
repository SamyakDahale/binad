import streamlit as st
import folium
from streamlit_folium import st_folium
from firebase_init import ref

# if "user_logged_in" not in st.session_state or not st.session_state["user_logged_in"]:
#     st.warning("Please login first.")
#     st.stop()

st.title("Admin - View & Edit Bins")

bins_ref = ref.get()

if bins_ref:
    # Initialize map
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

    bin_id_to_data = {}  # To reference bin data later

    for bin_id, bin_data in bins_ref.items():
        lat = bin_data['location']['lat']
        lon = bin_data['location']['lon']
        bin_type = bin_data['type']
        fill_percentage = bin_data['fill_percentage']

        # Create popup and tooltip
        popup_text = (
            f"ID: {bin_id}\nType: {bin_type}\nFill %: {fill_percentage}%"
        )
        tooltip_text = (
            f"Type: {bin_type} | Fill %: {fill_percentage}%"
        )

        folium.Marker(
            location=[lat, lon],
            popup=popup_text,
            tooltip=tooltip_text,  # Show type and fill % on hover
            icon=folium.Icon(color="green" if fill_percentage < 50 else "red")
        ).add_to(m)

        bin_id_to_data[bin_id] = bin_data

    # Show interactive map
    st.write("🗺️ Click a marker on the map to select a bin.")
    map_data = st_folium(m, height=500, width=700)

    # Get the clicked bin ID from popup text
    selected_bin_id = None
    if map_data and map_data.get("last_object_clicked_popup"):
        popup_text = map_data["last_object_clicked_popup"]
        if popup_text.startswith("ID:"):
            selected_bin_id = popup_text.replace("ID:", "").split()[0].strip()

    if selected_bin_id:
        selected_data = bin_id_to_data[selected_bin_id]

        # Allow admin to edit the selected bin
        new_type = st.selectbox("Update Type", ["Plastic", "Paper", "Organic", "Metal"],
                                index=["Plastic", "Paper", "Organic", "Metal"].index(selected_data['type']))
        new_fill = st.slider("Update Fill Percentage", 0, 100, int(selected_data['fill_percentage']))

        if st.button("Update Bin"):
            update_data = {
                'location': selected_data['location'],
                'type': new_type,
                'fill_percentage': new_fill
            }

            ref.child(selected_bin_id).update(update_data)
            st.success("✅ Bin updated successfully.")
            st.rerun()
else:
    st.write("No bins added yet.")
