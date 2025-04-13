#Importing necessary packages
import requests
import json
import os
import pandas as pd

#API endpoint (URL) for Firestore to fetch data
endpoint_url = "https://firestore.googleapis.com/v1/projects/rn-firebase-ml-test/databases/(default)/documents/patientData"

#Output path to store the fetched data
json_output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'patient_data.json')

#Fetching data from Firebase
response = requests.get(endpoint_url)
data = response.json()

#Saving the data to a JSON file
with open(json_output_path, 'w') as f:
    json.dump(data, f, indent=2)