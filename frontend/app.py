#Importing Necessary Packages
import streamlit as st
import pandas as pd
import plotly.express as px

# Set Streamlit layout to wide
st.set_page_config(layout="wide")

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

# Section 5 & 6: Sleep Duration and Interruptions vs Sleep Quality
st.subheader('Sleep Quality Analysis')

# Ensure the sleep_quality column is ordered correctly
ordered_categories = ['poor', 'fair', 'good', 'excellent']
data['sleep_quality'] = pd.Categorical(data['sleep_quality'], categories=ordered_categories, ordered=True)
data_sorted = data.sort_values('sleep_quality')

# Create the two charts
fig3 = px.box(
    data_sorted,
    x='sleep_quality',
    y='sleep_duration_hours',
    color='sleep_quality',
    title='Sleep Duration Distribution Across Sleep Quality Categories',
    labels={'sleep_quality': 'Sleep Quality', 'sleep_duration_hours': 'Sleep Duration (hrs)'}
)

fig4 = px.bar(
    data_sorted,
    x='sleep_quality',
    y='sleep_interruptions',
    color='sleep_quality',
    title='Sleep Interruptions Across Sleep Quality Categories',
    labels={'sleep_quality': 'Sleep Quality', 'sleep_interruptions': 'Sleep Interruptions'}
)

# Remove unsupported properties
fig4.update_traces(
    jitter=0.5,
    marker=dict(size=6),  # Removed 'color' and 'colorscale'
    selector=dict(type='violin')
)

# Display side-by-side in two columns
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig3, use_container_width=True, key="fig3")

with col2:
    st.plotly_chart(fig4, use_container_width=True, key="fig4")


# Section 7: Activity Analysis
st.subheader('Activity Metrics Analysis')

st.markdown("#### Steps in Active Minutes")
fig_activity_trend = px.bar(data, x='activity_active_minutes', y = 'activity_steps')
fig_activity_trend.update_layout(yaxis_title="Active Steps")
fig_activity_trend.update_layout(xaxis_title="Active Minutes")
st.plotly_chart(fig_activity_trend)

# --- Scatter Plot: Sedentary Hours vs Active Minutes ---
st.markdown("#### Sedentary vs Active Minutes")
fig_scat = px.scatter(
    data,
    x='activity_sedentary_hours',
    y='activity_active_minutes',
    color='sleep_quality',
    size='activity_steps',
    hover_data=['date'],
    title='Sedentary Hours vs Active Minutes (Bubble Size = Steps)',
    labels={
        'activity_sedentary_hours': 'Sedentary Hours',
        'activity_active_minutes': 'Active Minutes',
        'activity_steps': 'Steps'
    }
)
st.plotly_chart(fig_scat, use_container_width=True)

# --- Box Plot: Steps by Sleep Quality ---
st.markdown("#### Activity Steps Across Sleep Quality Levels")
fig_box_steps = px.box(
    data_sorted,
    x='sleep_quality',
    y='activity_steps',
    color='sleep_quality',
    title='Steps Distribution Across Sleep Quality Categories',
    labels={'activity_steps': 'Steps', 'sleep_quality': 'Sleep Quality'}
)
st.plotly_chart(fig_box_steps, use_container_width=True)