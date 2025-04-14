#Importing Necessary Packages
import streamlit as st
import pandas as pd
import plotly.express as px

#Loading the csv data
#Function
@st.cache_data
def load_data():
    df = pd.read_csv(r'C:\Projects\a_health_data_analysis\firebase-health-data-analysis\data\final_processed_data.csv')
#Converting the 'date' column to datetime format for plotting
    df['date'] = pd.to_datetime(df['date'], dayfirst=True)
    return df
data = load_data()

#Adding a header and description for the Dashboard 
st.title('Patient Health Dashboard')
st.write('Explore patient health data through various visualisations')

#Section 1: Showing the Data as a Table
if st.checkbox('Show raw data'):
    st.write(data)

#Section 2: Creating a Heart Rate Chart
st.subheader('Heart Rate Over Time')

#Calculating the average heart rate from the heart rate columns
heart_rate_columns = [col for col in data.columns if col.startswith('vitals_heart_rate')]
data['avg_heart_rate'] = data[heart_rate_columns].mean(axis=1)

#Creating a line chart for average heart rate
fig = px.line(data, x='date', y='avg_heart_rate', title='Average Heart Rate Over Time')
st.plotly_chart(fig)

#Section 3: Creating Sleep Duration Chart
st.subheader('Sleep Duration')
fig2 = px.bar(data, x='date', y='sleep_duration_hours', title='Sleep Duration Over Time')
st.plotly_chart(fig2)

#Section 4: Creating Vitals Table 
st.subheader('Vitals Table')
vitals_columns = ['date', 'avg_heart_rate', 'sleep_duration_hours', 'activity_active_minutes', 'activity_steps']
st.write(data[vitals_columns])