import streamlit as st
import os

import helper
from LLM_Geo_kernel import Solution


st.title("GeoCopilot")

## ========================== input section ================================
# default value
st.session_state['task_name'] = 'Resident_at_risk_counting'

st.session_state['TASK'] = r"""1) Find out Census tracts that contain hazardous waste facilities, then comppute and print out the population living in those tracts. The study area is North Carolina (NC), US.
2) Generate a population choropleth map for all tract polygons in NC, rendering the color by population; and then highlight the borders of tracts that have hazardous waste facilities. Please draw all polygons, not only the highlighted ones. The map size is 15*10 inches.
"""
st.session_state['DATA_LOCATIONS'] = [
    "NC hazardous waste facility ESRI shape file: https://github.com/gladcolor/LLM-Geo/raw/master/overlay_analysis/HW_Sites_EPSG4326.zip.",
    "NC tract boundary shapefile: https://github.com/gladcolor/LLM-Geo/raw/master/overlay_analysis/tract_37_EPSG4326.zip. The tract ID column is 'GEOID', data types is integer.",
    "NC tract population CSV file: https://github.com/gladcolor/LLM-Geo/raw/master/overlay_analysis/NC_tract_population.csv. The population is stored in 'TotalPopulation' column. The tract ID column is 'GEOID', data types is integer."
]
if 'DATA_LOCATIONS' not in st.session_state:
    st.session_state['DATA_LOCATIONS'] = []

# several input text areas
st.session_state['task_name'] = st.text_input("Name of task", value=st.session_state['task_name'])

st.session_state['TASK'] = st.text_input("task definition", value=st.session_state['TASK'])

for index, location in enumerate(st.session_state['DATA_LOCATIONS']):
    location = st.text_input(f"Enter the data location {index+1}", key=index, value=location)

# Button to add the new data location to the list
if st.button("Add Data Location"):    
    st.session_state['DATA_LOCATIONS'].append('')
    # Clear the input box after adding
    st.rerun()


## ========================= initialize solution ===================
save_dir = os.path.join(os.getcwd(), 'solutions', st.session_state['task_name'])
os.makedirs(save_dir, exist_ok=True)

# create graph
model=r"gpt-4"
solution = Solution(
                    task=st.session_state['TASK'],
                    task_name=st.session_state['task_name'],
                    save_dir=save_dir,
                    data_locations=st.session_state['DATA_LOCATIONS'],
                    model=model,
                    )

## ============================ Graph ==========================
if st.button("Generate operation graph"):
    response_for_graph = solution.get_LLM_response_for_graph() 
    solution.graph_response = response_for_graph
    st.write(response_for_graph)