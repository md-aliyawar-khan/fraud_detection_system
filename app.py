from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib
import os
import numpy as np
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# Load the trained model
def load_model():
    """Load the trained fraud detection model"""
    try:
        model_path = os.path.join(os.path.dirname(__file__), 'models', 'fraud_detection_model.pkl')
        model = joblib.load(model_path)
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

# Load the scaler (you'll need to save this during training)
def load_scaler():
    """Load the StandardScaler used during training"""
    try:
        scaler_path = os.path.join(os.path.dirname(__file__), 'models', 'scaler.pkl')
        scaler = joblib.load(scaler_path)
        return scaler
    except Exception as e:
        print(f"Error loading scaler: {e}")
        return None

# Initialize model and scaler
model = load_model()
scaler = load_scaler()
model_feature_columns = list(getattr(model, "feature_names_in_", [])) if model is not None else []

@app.route('/')
def home():
    """Home endpoint with web interface"""
    return render_template('index.html')

@app.route('/api')
def api_info():
    """API information endpoint"""
    return jsonify({
        'message': 'Fraud Detection API',
        'version': '1.0.0',
        'endpoints': {
            '/predict': 'POST - Predict fraud for a single transaction',
            '/predict_batch': 'POST - Predict fraud for multiple transactions',
            '/health': 'GET - API health check'
        }
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    if model is None:
        return jsonify({'status': 'error', 'message': 'Model not loaded'}), 500
    
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'scaler_loaded': scaler is not None
    })

@app.route('/predict', methods=['POST'])
def predict_fraud():
    """Predict fraud for a single transaction"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract features (excluding 'id' and 'Class' if present)
        required_features = ['V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10',
                           'V11', 'V12', 'V13', 'V14', 'V15', 'V16', 'V17', 'V18', 'V19',
                           'V20', 'V21', 'V22', 'V23', 'V24', 'V25', 'V26', 'V27', 'V28', 'Amount']
        
        # Check if all required features are present
        missing_features = [feature for feature in required_features if feature not in data]
        if missing_features:
            return jsonify({'error': f'Missing features: {missing_features}'}), 400
        
        # Build base frame from expected request features
        df = pd.DataFrame([[data[feature] for feature in required_features]], columns=required_features)
        
        # Scale the Amount feature if scaler is available
        if scaler is not None:
            df['Amount'] = scaler.transform(df[['Amount']])
        
        # Align request features with model training schema (e.g., model trained with extra id column)
        if model_feature_columns:
            for column in model_feature_columns:
                if column not in df.columns:
                    df[column] = 0.0
            df = df[model_feature_columns]

        # Make prediction
        prediction = model.predict(df)[0]
        prediction_proba = model.predict_proba(df)[0]
        
        # Return prediction with confidence
        result = {
            'fraud_detected': bool(prediction),
            'confidence': float(max(prediction_proba)),
            'fraud_probability': float(prediction_proba[1]),
            'non_fraud_probability': float(prediction_proba[0])
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Prediction error: {str(e)}'}), 500

@app.route('/predict_batch', methods=['POST'])
def predict_batch():
    """Predict fraud for multiple transactions"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data or 'transactions' not in data:
            return jsonify({'error': 'No transactions data provided'}), 400
        
        transactions = data['transactions']
        
        if not isinstance(transactions, list):
            return jsonify({'error': 'Transactions must be a list'}), 400
        
        required_features = ['V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10',
                           'V11', 'V12', 'V13', 'V14', 'V15', 'V16', 'V17', 'V18', 'V19',
                           'V20', 'V21', 'V22', 'V23', 'V24', 'V25', 'V26', 'V27', 'V28', 'Amount']
        
        results = []
        
        for i, transaction in enumerate(transactions):
            try:
                # Check if all required features are present
                missing_features = [feature for feature in required_features if feature not in transaction]
                if missing_features:
                    results.append({
                        'index': i,
                        'error': f'Missing features: {missing_features}'
                    })
                    continue
                
                # Build base frame from expected request features
                df = pd.DataFrame(
                    [[transaction[feature] for feature in required_features]],
                    columns=required_features
                )
                
                # Scale the Amount feature if scaler is available
                if scaler is not None:
                    df['Amount'] = scaler.transform(df[['Amount']])
                
                # Align request features with model training schema (e.g., model trained with extra id column)
                if model_feature_columns:
                    for column in model_feature_columns:
                        if column not in df.columns:
                            df[column] = 0.0
                    df = df[model_feature_columns]

                # Make prediction
                prediction = model.predict(df)[0]
                prediction_proba = model.predict_proba(df)[0]
                
                results.append({
                    'index': i,
                    'fraud_detected': bool(prediction),
                    'confidence': float(max(prediction_proba)),
                    'fraud_probability': float(prediction_proba[1]),
                    'non_fraud_probability': float(prediction_proba[0])
                })
                
            except Exception as e:
                results.append({
                    'index': i,
                    'error': f'Prediction error: {str(e)}'
                })
        
        return jsonify({'predictions': results})
        
    except Exception as e:
        return jsonify({'error': f'Batch prediction error: {str(e)}'}), 500

if __name__ == '__main__':
    # Check if model is loaded
    if model is None:
        print("Warning: Model not loaded. Please ensure the model file exists.")
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 