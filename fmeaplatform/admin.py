import streamlit as st
import pandas as pd
import altair as alt

alt.themes.enable("dark")
# Load the dataset
@st.cache
def load_data():
    return pd.read_csv('BMW_Car_Problems_500_Instances_Updated.csv')

df = load_data()

# Sidebar filters
st.sidebar.header('Filter Options')
selected_car_name = st.sidebar.multiselect('Car Name', options=df['Car name'].unique())
selected_car_model = st.sidebar.multiselect('Car Model', options=df['Car model'].unique())
selected_problem = st.sidebar.multiselect('Problem', options=df['Problem'].unique())
selected_failure_mode = st.sidebar.multiselect('Failure Mode', options=df['Failure Mode'].unique())

# Filtering data
if selected_car_name:
    df = df[df['Car name'].isin(selected_car_name)]
if selected_car_model:
    df = df[df['Car model'].isin(selected_car_model)]
if selected_problem:
    df = df[df['Problem'].isin(selected_problem)]
if selected_failure_mode:
    df = df[df['Failure Mode'].isin(selected_failure_mode)]

# Severity and Occurrence sliders
severity = st.sidebar.slider('Severity', 1, 10, (1, 10))
occurrence = st.sidebar.slider('Occurence', 1, 10, (1, 10))
df = df[(df['Severity'] >= severity[0]) & (df['Severity'] <= severity[1])]
df = df[(df['Occurence'] >= occurrence[0]) & (df['Occurence'] <= occurrence[1])]

# Display data
st.dataframe(df)

# Run this script using:
# streamlit run script_name.py
