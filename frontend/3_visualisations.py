#Importing Necessary Packages
import streamlit as st
import pandas as pd
import plotly.express as px

# Set Streamlit layout to wide
st.set_page_config(layout="wide")

#Loading the csv data
#Function to load the data
@st.cache_data
def load_data():
    return pd.read_csv('data/cleaned_data.csv')


#Loading the csv data
data = load_data()

#Adding a header and description for the Dashboard 
st.title('Patient Health Dashboard')
#st.write('Exploring patient health data through various visualisations')

#Section 1: Showing the Data as a Table
if st.checkbox('Displaying raw data as table'):
    st.write(data)

#Section 2: Creating a Heart Rate Chart - Avg Heart Rate vs Sleep Duration
#st.subheader('Heart Rate vs Sleep Duration')
fig_heart_rate_sleep = px.scatter(
    data,
    x='avg_heart_rate',
    y='sleep_duration_hours',
    color='sleep_quality',
    title='Heart Rate vs Sleep Duration',
    labels={'avg_heart_rate': 'Heart Rate', 'sleep_duration_hours': 'Sleep Duration (hrs)'}
)
st.plotly_chart(fig_heart_rate_sleep, use_container_width=True)

#Section 3: Creating Sleep Duration Chart - Avg Temperature vs Sleep Interruptions
#st.subheader('Avg Temperature vs Sleep Interruptions')
fig_temp_sleep_interrupt = px.scatter(
    data,
    x='avg_temperature',
    y='sleep_interruptions',
    color='sleep_quality',
    title='Temperature vs Sleep Interruptions',
    labels={'avg_temperature': 'Temperature', 'sleep_interruptions': 'Sleep Interruptions'}
)
st.plotly_chart(fig_temp_sleep_interrupt, use_container_width=True)

#Section 4: Creating Vitals Table - Avg BP vs Activity Steps
#st.subheader('Blood Pressure vs Activity')
# Split systolic and diastolic for better clarity
data[['avg_systolic_bp', 'avg_diastolic_bp']] = data['avg_bp'].str.split('/', expand=True).astype(float)
fig_bp_activity = px.scatter(
    data,
    x='activity_steps',
    y='avg_systolic_bp',
    color='sleep_quality',
    title='Blood Pressure vs Activity Steps (Systolic)',
    labels={'activity_steps': 'Activity Steps', 'avg_systolic_bp': 'Systolic Blood Pressure (mmHg)'}
)
st.plotly_chart(fig_bp_activity, use_container_width=True)

# Bar chart: BP grouped by Sleep Quality
avg_bp_by_sleep = data.groupby('sleep_quality')[['avg_systolic_bp', 'avg_diastolic_bp']].mean().reset_index()
fig_bp_bar = px.bar(
    avg_bp_by_sleep,
    x='sleep_quality',
    y=['avg_systolic_bp', 'avg_diastolic_bp'],
    barmode='group',
    title='Average Blood Pressure by Sleep Quality',
    labels={'value': 'Blood Pressure', 'sleep_quality': 'Sleep Quality'}
)
st.plotly_chart(fig_bp_bar, use_container_width=True)

mean_protein = data['nutrition_macro_protein_g'].mean()
mean_carbs = data['nutrition_macro_carbs_g'].mean()
mean_fat = data['nutrition_macro_fat_g'].mean()

fig_macro_ratio = px.pie(
    names=['Protein', 'Carbs', 'Fat'],
    values=[mean_protein, mean_carbs, mean_fat],
    title='Average Macronutrient Ratio'
)
st.plotly_chart(fig_macro_ratio)

#Section 5 & 6: Sleep Duration and Interruptions vs Sleep Quality
st.subheader('Sleep Quality Analysis')

#Ensure the sleep_quality column is ordered correctly
ordered_categories = ['poor', 'fair', 'good', 'excellent']
data['sleep_quality'] = pd.Categorical(data['sleep_quality'], categories=ordered_categories, ordered=True)
data_sorted = data.sort_values('sleep_quality')

#Create the two charts
fig3 = px.box(
    data_sorted,
    x='sleep_quality',
    y='sleep_duration_hours',
    color='sleep_quality',
    title='Sleep Duration Distribution Across Sleep Quality',
    labels={'sleep_quality': 'Sleep Quality', 'sleep_duration_hours': 'Sleep Duration (hrs)'}
)

fig4 = px.box(
    data_sorted,
    x='sleep_quality',
    y='sleep_interruptions',
    color='sleep_quality',
    title='Sleep Interruptions Across Sleep Quality',
    labels={'sleep_quality': 'Sleep Quality', 'sleep_interruptions': 'Sleep Interruptions'}
)
fig4.update_traces(
    jitter=0.5,
    marker=dict(size=6),  # 
    selector=dict(type='violin')
)
#Display side-by-side in two columns
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig3, use_container_width=True, key="fig3")

with col2:
    st.plotly_chart(fig4, use_container_width=True, key="fig4")


#Section 7: Activity Analysis
st.subheader('Activity Metrics Analysis')
#st.markdown("#### Steps in Active Minutes")
fig_activity_trend = px.scatter(data, x='activity_active_minutes', y='activity_steps',title='Steps in Active Minutes')
fig_activity_trend.update_layout(
    yaxis_title="Steps",
    yaxis=dict(tickformat=',')  #keeping numbers with commas, e.g., 10,000 instead of 10k
)
fig_activity_trend.update_layout(xaxis_title="Active Minutes")
st.plotly_chart(fig_activity_trend)

#Scatter Plot: Sedentary Hours vs Active Minutes
#st.markdown("#### Sedentary vs Active Minutes")
fig_scat = px.scatter(
    data,
    x='activity_sedentary_hours',
    y='activity_active_minutes',
    color='sleep_quality',
    size='activity_steps',
    title='Sedentary Hours vs Active Minutes (Bubble Size = Steps)',
    labels={
        'activity_sedentary_hours': 'Sedentary Hours',
        'activity_active_minutes': 'Active Minutes',
        'activity_steps': 'Steps'
    }
)
st.plotly_chart(fig_scat, use_container_width=True)

# --- Box Plot: Steps by Sleep Quality ---
#st.markdown("#### Activity Steps Across Sleep Quality Levels")
fig_box_steps = px.box(
    data_sorted,
    x='sleep_quality',
    y='activity_steps',
    color='sleep_quality',
    title='Steps Distribution Across Sleep Quality',
    labels={'activity_steps': 'Steps', 'sleep_quality': 'Sleep Quality'}
)
st.plotly_chart(fig_box_steps, use_container_width=True)