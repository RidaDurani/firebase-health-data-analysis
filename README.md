# Patient Health Data Analysis and Classification

This project focuses on analysing health data, visualising key trends, and building a machine learning model to classify health conditions into three categories: "Poor," "Moderate," and "Good".

## **Project Structure**

1. **Data Fetching**: Data was fetched from a Firebase database and then pre-processed.

2. **Data Cleaning**: Removed irrelevant or missing records, handled missing values, and formatted the dataset for analysis.

3. **Visualization**: Key trends in the dataset were visualized using Streamlit for an interactive experience.

4. **Model Training**: Built a machine learning model for health classification using scikit-learn.

 

---

 

## **Steps and Tools**

 

### **1. Data Fetching and Cleaning**

- Loaded the dataset from Firebase and saved it as `cleaned_data.csv`.

- Addressed missing values and formatted columns for consistency.

- Labelled data into health categories using the `classify_health` function.

 

### **2. Visualization**

- Built an interactive dashboard using **Streamlit**.

- Key visualizations:

  - Sleep duration vs. sleep quality

  - Activity levels vs. sedentary hours

  - Macronutrient analysis

 

### **3. Model Training**

- Preprocessed data with:

  - **One-Hot Encoding** for categorical features.

  - **Scaling** using `StandardScaler`.

- Splitted into training and testing sets (80:20).

- Trained a machine learning model for classification:

  - Used Random Forest for its robustness.

  - Achieved 100% accuracy on the test set.

 

### **4. Evaluation**

- Metrics:

  - **Confusion Matrix**: Evaluated model performance visually.

  - **Feature Importance**: Identified top predictors for health classification.

- Exported final model for deployment.

 

---

### **Requirements**

- Python 3.9 or higher

- Python packages required to run the code:
 - Pandas - pip install
 - Numpy
 - Matplotlib
 - Seaborn
 - Streamlit
 - Plotly

Once you have install python packages on your setup, run this command on your terminal: streamlit run frontend/3_visualisations.py

### **Setup**

1. Clone the repository: 

   ```bash

   git clone https://github.com/RidaDurani/firebase-health-data-analysis.git

2. Dashboard Link:

```bash
dashboard: https://firebase-health-data-analysis-nxt3ajm7cwtegsbpcuk6ij.streamlit.app/


