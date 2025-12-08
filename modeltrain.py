import pandas as pd
from catboost import CatBoostClassifier
import joblib # Used for saving scikit-learn related items
import os

# --- 1. Train Final Model on ALL Data ---

# Define the data setup (same cleaning/imputation as training)
df =  pd.read_csv(r"C:\Users\Gurleen Kaur\Downloads\osteoporosis.csv")
df = df.drop(columns=['Id'])
df['Alcohol Consumption'] = df['Alcohol Consumption'].fillna('No_Alcohol')
df['Medical Conditions'] = df['Medical Conditions'].fillna('None')
df['Medications'] = df['Medications'].fillna('None')
df.drop_duplicates(inplace=True)

# Define X and y for full training
X_full = df.drop(columns=['Osteoporosis'])
y_full = df['Osteoporosis']

# Identify categorical features for CatBoost
CAT_FEATURES_NAMES = X_full.select_dtypes(include='object').columns.tolist()

# Define the final CatBoost model configuration
final_catboost_model = CatBoostClassifier(
    verbose=0,
    random_state=42,
    n_estimators=300,
    cat_features=CAT_FEATURES_NAMES, # Use feature names for prediction robustness
    auto_class_weights="Balanced"
)

# Train the model on the entire dataset
print("Training final CatBoost model on all data...")
final_catboost_model.fit(X_full, y_full)
print("Training complete.")

# --- 2. Save the Trained Model ---
# Save the model to a file that can be loaded by your website backend (e.g., Flask/Django)
MODEL_FILE = 'final_catboost_model.cbm'
final_catboost_model.save_model(MODEL_FILE)
print(f"Final model saved to {MODEL_FILE}")

# ----------------------------------------------------------------
# B. Prediction Function for Website Backend
# ----------------------------------------------------------------

def predict_osteoporosis_risk(raw_input_data):
    """
    Loads the saved CatBoost model and makes a prediction based on raw user input.
    
    Args:
        raw_input_data (dict): A dictionary mapping feature names to user input values.
        Example: {'Age': 60, 'Gender': 'Female', 'Smoking': 'Yes', ...}
    
    Returns:
        tuple: (prediction_result, confidence_score)
    """
    # 1. Load the model
    loaded_model = CatBoostClassifier()
    loaded_model.load_model(MODEL_FILE)
    
    # 2. Convert input data to DataFrame (ensuring correct order/columns)
    input_df = pd.DataFrame([raw_input_data])
    
    # 3. Apply the same IMPUTATION logic as training (CRITICAL STEP!)
    # CatBoost expects the data types to match the training data.
    input_df['Alcohol Consumption'] = input_df['Alcohol Consumption'].fillna('No_Alcohol')
    input_df['Medical Conditions'] = input_df['Medical Conditions'].fillna('None')
    input_df['Medications'] = input_df['Medications'].fillna('None')
    
    # 4. Make prediction
    # CatBoost handles the categorical values directly
    prediction = loaded_model.predict(input_df)[0]
    
    # Get probability for confidence
    confidence = loaded_model.predict_proba(input_df)[0][1] # Probability of Class 1 (Osteoporosis)
    
    result = "Osteoporosis Risk Detected" if prediction == 1 else "Low Osteoporosis Risk"
    
    return result, confidence

# Example Usage (Simulating Website Input):
user_input = {
    'Age': 75, 
    'Gender': 'Female', 
    'Hormonal Changes': 'Postmenopausal', 
    'Family History': 'Yes', 
    'Race/Ethnicity': 'Caucasian', 
    'Body Weight': 'Underweight', 
    'Calcium Intake': 'Low', 
    'Vitamin D Intake': 'Insufficient', 
    'Physical Activity': 'Sedentary', 
    'Smoking': 'Yes', 
    'Alcohol Consumption': None, # Simulate missing input
    'Medical Conditions': 'Rheumatoid Arthritis', 
    'Medications': 'Corticosteroids', 
    'Prior Fractures': 'Yes'
}
prediction, confidence = predict_osteoporosis_risk(user_input)
print(f"\nUser Prediction: {prediction} with Confidence: {confidence:.2f}")