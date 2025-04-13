#Importing necessary packages
import pandas as pd
import json

#Loading the JSON data
with open('C:\\Users\\Rida.KD\\Projects\\a_health_data_analysis\\firebase-health-data-analysis\\data\\patient_data.json') as f:
    data = json.load(f)

records = data["documents"]
#Looking at the first record present in the json file to understand the structure of the data
#pprint.pprint(records[0]) 

#Function to extract field values from the json data
def extract_value(field):
    if "stringValue" in field:
        return field["stringValue"]
    elif "integerValue" in field:
        return int(field["integerValue"])
    elif "doubleValue" in field:
        return float(field["doubleValue"])
    elif "arrayValue" in field:
        return [extract_value(val) for val in field["arrayValue"].get("values", [])]
    elif "mapValue" in field:
        return {k: extract_value(v) for k, v in field["mapValue"]["fields"].items()}
    else:
        return None

#Flattening the high level fields
flat_records = []

for doc in records:
    fields = doc["fields"]
    flat = {k: extract_value(v) for k, v in fields.items()}
    
    #Flattening fields within sleep 
    sleep = flat.pop("sleep", {})
    if isinstance(sleep, dict):
        for k, v in sleep.items():
            flat[f"sleep_{k}"] = v
    
    #Flattening fields within activity 
    activity = flat.pop("activity", {})
    if isinstance(activity, dict):
        for k, v in activity.items():
            flat[f"activity_{k}"] = v
    
    #Flattening fields within nutrition
    nutrition = flat.pop("nutrition", {})
    if isinstance(nutrition, dict):
        macros = nutrition.pop("macros", {})
        for k, v in nutrition.items():
            flat[f"nutrition_{k}"] = v
        if isinstance(macros, dict):
            for k, v in macros.items():
                flat[f"nutrition_macro_{k}"] = v

    #Extracting the further field values in the fields
    vitals = flat.pop("vitals", {})
    heart_rate = vitals.get("heart_rate", [])
    bp = vitals.get("blood_pressure", [])
    temp = vitals.get("temperature", [])
    
    #Flattening fields within vitals
    flat["vitals_heart_rate_mean"] = heart_rate
    flat["vitals_bp_latest"] = bp
    flat["vitals_temp_max"] = temp

    #Adding the flattened record to the list
    flat_records.append(flat)

#Converting the flattened data into a DataFrame
proccessed_df = pd.DataFrame(flat_records)

#Saving the processed data to a CSV file
proccessed_df.to_csv('C:\\Users\\Rida.KD\\Projects\\a_health_data_analysis\\firebase-health-data-analysis\\data\\processed_data.csv', index=False)