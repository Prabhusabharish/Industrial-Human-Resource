import streamlit as st
import pandas as pd
from PIL import Image
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from streamlit_option_menu import option_menu
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns


#-------------------------------------------------------------------------------------------


# - - - - - - - - - - - - - - -set st addbar page - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

icon = Image.open("C:/Users/prabh/Downloads/Datascience/Project/CT/1.png")
st.set_page_config(page_title= "HRM", page_icon= icon, layout= "wide", initial_sidebar_state= "expanded",
                   menu_items={'About': """# This Flat Resale page is created by *Prabakaran!"""})
st.markdown("<h1 style='text-align: center; color: black;'>Industrial Human Resource Geo-Visualization</h1>", unsafe_allow_html=True)

#----------------------------------------------------------------------------------------------------------------------------------

# SELECT = option_menu(
#     menu_title=None,
#     options=["Charts & Plots", "Geo - Maps"],
#     default_index=0,
#     orientation="horizontal",
#     styles={"container": {"padding": "0!important", "background-color": "white", "size": "cover", "width": "100"},
#             "icon": {"color": "black", "font-size": "20px"},

#             "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#6F36AD"},
#             "nav-link-selected": {"background-color": "#6F36AD"}})


#----------------------------------------------------------------------------------------------------------------------------------
# if SELECT == "Charts & Plots":

data = pd.read_csv("C:/Users/prabh/Downloads/Datascience/Project/CT/final_HR.csv")

unique_states = sorted(data['State'].unique())
selected_state = st.sidebar.selectbox("Select State", unique_states, key="state_selector")

# Filter districts based on the selected state
filtered_districts = sorted(data[data['State'] == selected_state]['District'].unique())
selected_district = st.sidebar.selectbox("Select District", filtered_districts, key="district_selector")

filtered_nic_names = data[data['District'] == selected_district]['NICName'].unique()
filtered_nic_names = [nic.replace('[', '').replace(']', '').replace("'", "") for nic in filtered_nic_names]
filtered_nic_names = [nic.capitalize() for nic in filtered_nic_names]
filtered_nic_names = sorted(filtered_nic_names)

selected_nic_name = st.sidebar.selectbox("Select NIC Name", filtered_nic_names, key="nic_name_selector")

# #------------------------------------------------------------------------------------------------


# Plotting data for Rural, Main, and Urban workers
rural_cols = ['MainWorkersRuralPersons', 'MainWorkersRuralMales', 'MainWorkersRuralFemales']
urban_cols = ['MainWorkersUrbanPersons', 'MainWorkersUrbanMales', 'MainWorkersUrbanFemales']

rural_data = data[rural_cols].sum().values
main_data = data[['MainWorkersTotalPersons', 'MainWorkersTotalMales', 'MainWorkersTotalFemales']].iloc[0].values
urban_data = data[urban_cols].sum().values

fig, ax = plt.subplots(figsize=(10, 6))
x_labels = ['Rural', 'Main', 'Urban']
ax.bar(x_labels, rural_data, color='#1f77b4', label='Rural')
ax.bar(x_labels, main_data, bottom=rural_data, color='#ff7f0e', label='Main')
ax.bar(x_labels, urban_data, bottom=rural_data + main_data, color='#2ca02c', label='Urban')
ax.set_title(f"{selected_state} - {selected_district} - Workers Distribution")
ax.legend()
st.pyplot(fig)


#---------------------------------------------------------------------------------------------

# Plotting data for Marginal workers (using pie chart)
marginal_cols_rural = ['MarginalWorkersRuralPersons', 'MarginalWorkersRuralMales', 'MarginalWorkersRuralFemales']
marginal_cols_urban = ['MarginalWorkersUrbanPersons', 'MarginalWorkersUrbanMales', 'MarginalWorkersUrbanFemales']

marginal_data_rural = data[marginal_cols_rural].sum().values
marginal_data_urban = data[marginal_cols_urban].sum().values

fig, ax = plt.subplots(figsize=(10, 6))
ax.pie(marginal_data_rural, labels=marginal_cols_rural, autopct='%1.1f%%', startangle=90, colors=['#1f77b4', '#ff7f0e', '#2ca02c'])
ax.set_title(f"{selected_state} - {selected_district} - Rural Marginal Workers Distribution")
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(10, 6))
ax.pie(marginal_data_urban, labels=marginal_cols_urban, autopct='%1.1f%%', startangle=90, colors=['#1f77b4', '#ff7f0e', '#2ca02c'])
ax.set_title(f"{selected_state} - {selected_district} - Urban Marginal Workers Distribution")
st.pyplot(fig)

#---------------------------------------------------------------------------------------------

# if SELECT == "Geo - Maps":

data = pd.read_csv("C:/Users/prabh/Downloads/Datascience/Project/CT/final_HR.csv")

state_data = data[(data['State'] == selected_state)]
district_data = data[(data['District'] == selected_district)]

folium_map = folium.Map(location=[28.6139, 77.2090], zoom_start=5)

marker_cluster = MarkerCluster().add_to(folium_map)

for idx, row in state_data.iterrows():
    lat, lon = row['latitude'], row['longitude']
    total_workers = row['MainWorkersTotalPersons']
    male_female_ratio = row['MaleFemaleRatio']
    popup_text = f"State: {selected_state}<br>District: {selected_district}<br>Total Workers: {total_workers}<br>Male-Female Ratio: {male_female_ratio}"
    folium.Marker([lat, lon], popup=popup_text).add_to(marker_cluster)

for idx, row in district_data.iterrows():
    lat, lon = row['latitude'], row['longitude']
    total_workers = row['MainWorkersTotalPersons']
    male_female_ratio = row['MaleFemaleRatio']
    popup_text = f"State: {selected_state}<br>District: {selected_district}<br>Total Workers: {total_workers}<br>Male-Female Ratio: {male_female_ratio}"
    folium.Marker([lat, lon], popup=popup_text).add_to(marker_cluster)

st.components.v1.html(folium_map._repr_html_(), width=700, height=500)

