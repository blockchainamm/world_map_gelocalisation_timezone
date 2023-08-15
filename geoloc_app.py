# Import required packages
from geopy.geocoders import ArcGIS
import folium
import streamlit as st
from streamlit_tags import st_tags
from streamlit_folium import st_folium
import pandas as pd
import geopandas as gpd
# from arcgis.geocoding import geocode
# from arcgis.gis import GIS

nom=ArcGIS()

# -------------- SETTINGS ----------------------------
page_title = "Geolocalisation and Timezone indicator"
layout = "centered"
# ----------------------------------------------------


def main():
    st.set_page_config(page_title = page_title, layout = layout)
    st.title(page_title)

if __name__ == '__main__':
    main()

# --- Hide Streamlit Style ---
hide_st_style = """
                <style>
                #MainMenu {Visibility: hidden;}
                footer {Visibility: hidden;}
                header {Visibility: hidden;}
                </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

nom=ArcGIS()

# Input place name as list in streamlit, maximum tabs is limited to 10
place_name = st_tags(
    label='## Enter place name:',
    text='Press enter to add more',
    value=['Chennai', 'Paris', 'London'],
    maxtags = 10,
    key='1')

# Convert List to a DataFrame
place_df = pd.DataFrame(place_name)

# Before renaming the columns
#print(place_df.columns)
  
place_df.columns = ['placename']
  
# After renaming the columns
#print(place_df.columns)

place_df['coordinates']=place_df['placename'].apply(nom.geocode)
#parcreg_df2['coordinates'].values

# Using lambda function to set the latitude of longitude in parc regional dataframe
place_df['latitude'] = place_df['coordinates'].apply(lambda x: x.latitude)
place_df['longitude'] = place_df['coordinates'].apply(lambda x: x.longitude)
"---"
st.write('Place name with coordinates data frame')
st.write(place_df)

# Create a list from place name dataframe with columns
# placename, latitude, and longitude
place_list = place_df[['placename', 'latitude', 'longitude']].values.tolist()

# Plotting place name in the map
m = folium.Map(location=[13.0838, 80.2826], zoom_start=2)
fg = folium.FeatureGroup(name = "Geolocation in world map")

"---"
st.write()
st.write('World map showing geo located coordinates of places')
for i in place_list:
    fg.add_child(
        folium.Marker(
            location=[i[1],i[2]],
            popup=f"{i[0]}\n {i[1]}°N\n {i[2]}°E\n",
            tooltip=f"{i[0]}",
            icon=folium.Icon(color="green")            
        )
    )

out = st_folium(
    m,
    feature_group_to_add=fg,
    width=1200,
    height=500,
)
