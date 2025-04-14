#Importing necessary packages
import pandas as pd
import json

#Loading the JSON data
with open('C:\\Projects\\a_health_data_analysis\\firebase-health-data-analysis\\data\\patient_data.json') as f:
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

    #Adding first level fields - metadata 
    flat["name"] = doc.get("name", "")
    flat["create_time"] = doc.get("createTime", "")
    flat["update_time"] = doc.get("updateTime", "")

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
    flat["vitals_heart_rate"] = heart_rate
    flat["vitals_bp"] = bp
    flat["vitals_temp"] = temp

    #Adding the flattened record to the list
    flat_records.append(flat)

#Converting the flattened data into a DataFrame
proccessed_df = pd.DataFrame(flat_records)

#Saving the processed data to a CSV file
proccessed_df.to_csv('C:\\Projects\\a_health_data_analysis\\firebase-health-data-analysis\\data\\processed_data.csv', index=False)

# Creating a new ID column from the 'name' field
proccessed_df['ID'] = proccessed_df['name'].apply(lambda x: x.split('/')[-1] if isinstance(x, str) else '')

# Expanding vitals_heart_rate to individual columns
for i in range(6):
    proccessed_df[f'vitals_heart_rate_{i+1}'] = proccessed_df['vitals_heart_rate'].apply(
        lambda x: x[i] if isinstance(x, list) and len(x) > i else None
    )

# Expanding vitals_bp to individual columns
for i in range(5):
    proccessed_df[f'vitals_bp_{i+1}'] = proccessed_df['vitals_bp'].apply(
        lambda x: x[i] if isinstance(x, list) and len(x) > i else None
    )

# Expanding vitals_temp to individual columns
for i in range(5):
    proccessed_df[f'vitals_temp_{i+1}'] = proccessed_df['vitals_temp'].apply(
        lambda x: x[i] if isinstance(x, list) and len(x) > i else None
    )

proccessed_df.drop(columns=['date','ID','name','create_time','update_time','vitals_heart_rate', 'vitals_bp', 'vitals_temp'], inplace=True)


#Calculating average of heart rate
heart_rate_cols = [col for col in proccessed_df.columns if col.startswith("vitals_heart_rate")]
proccessed_df["avg_heart_rate"] = proccessed_df[heart_rate_cols].mean(axis=1).round(2)

#Calculating average temperature
temp_cols = [col for col in proccessed_df.columns if col.startswith("vitals_temp")]
proccessed_df["avg_temperature"] = proccessed_df[temp_cols].mean(axis=1).round(2)

#Calculating average of bp
#Converting BP columns as spliting systolic/diastolic into separate columns
bp_cols = [col for col in proccessed_df.columns if col.startswith("vitals_bp")]
#Spliting BP into systolic and diastolic
for i, col in enumerate(bp_cols):
    proccessed_df[f'bp_sys_{i+1}'] = proccessed_df[col].str.split('/').str[0].astype(int)
    proccessed_df[f'bp_dia_{i+1}'] = proccessed_df[col].str.split('/').str[1].astype(int)
#Average systolic and diastolic separately
sys_cols = [col for col in proccessed_df.columns if col.startswith("bp_sys_")]
dia_cols = [col for col in proccessed_df.columns if col.startswith("bp_dia_")]
proccessed_df["avg_systolic_bp"] = proccessed_df[sys_cols].mean(axis=1).round(2)
proccessed_df["avg_diastolic_bp"] = proccessed_df[dia_cols].mean(axis=1).round(2)
#Combineing the two average BP values into one column as "systolic/diastolic"
proccessed_df["avg_bp"] = proccessed_df["avg_systolic_bp"].round(1).astype(str) + "/" + proccessed_df["avg_diastolic_bp"].round(1).astype(str)

#Selected Columns for more cleaned df
selected_columns = [
    "sleep_duration_hours",
    "sleep_quality",
    "sleep_interruptions",
    "activity_sedentary_hours",
    "activity_active_minutes",
    "activity_steps",
    "nutrition_calories",
    "nutrition_water_oz",
    "nutrition_macro_fat_g",
    "nutrition_macro_carbs_g",
    "nutrition_macro_protein_g",
    "avg_heart_rate",
    "avg_temperature",
    "avg_systolic_bp",
    "avg_diastolic_bp",
    "avg_bp"
]
df_selected = proccessed_df
df_selected = proccessed_df[selected_columns]

#Saving the processed data to a CSV file
proccessed_df.to_csv('C:\\Projects\\a_health_data_analysis\\firebase-health-data-analysis\\data\\final_processed_data.csv', index=False)
df_selected.to_csv('C:\\Projects\\a_health_data_analysis\\firebase-health-data-analysis\\data\\cleaned_data.csv', index=False)