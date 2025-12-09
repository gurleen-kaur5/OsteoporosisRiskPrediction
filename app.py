from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from catboost import CatBoostClassifier

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Load the model once when the server starts
MODEL_FILE = 'final_catboost_model.cbm'
model = CatBoostClassifier()
model.load_model(MODEL_FILE)
MODEL_METRICS = {
    'accuracy': 0.8849,  # Overall Correctness
    'precision': 1.0000, # Clinical Safety Guarantee (MUST be 1.0)
    'recall': 0.7704,    # Sensitivity
    'f1_score': 0.8703   # Balanced Performance
}
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data from request
        raw_input_data = request.get_json()
        
        # Convert to DataFrame
        input_df = pd.DataFrame([raw_input_data])
        
        # Apply imputation (same as training)
        input_df['Alcohol Consumption'] = input_df['Alcohol Consumption'].fillna('No_Alcohol')
        input_df['Medical Conditions'] = input_df['Medical Conditions'].fillna('None')
        input_df['Medications'] = input_df['Medications'].fillna('None')
        
        # Make prediction
        prediction = model.predict(input_df)[0]
        confidence = model.predict_proba(input_df)[0][1]
        
        result = "Osteoporosis Risk Detected" if prediction == 1 else "Low Osteoporosis Risk"
        
        return jsonify({
            'prediction': result,
            'confidence': float(confidence), 
            'metrics': MODEL_METRICS
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)