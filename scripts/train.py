import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
import joblib
import os

def load_processed_data(X_file_path, y_file_path):
    """
    Loads the preprocessed features and labels from the specified file paths.
    
    Parameters:
    - X_file_path: str, path to the preprocessed features (CSV).
    - y_file_path: str, path to the preprocessed labels (CSV).
    
    Returns:
    - X: DataFrame containing the features.
    - y: DataFrame containing the target labels.
    """
    print(f"Loading preprocessed data from {X_file_path} and {y_file_path}")
    X = pd.read_csv(X_file_path)
    y = pd.read_csv(y_file_path)
    return X, y

def train_model(X, y):
    """
    Trains a RandomForest model using the given features and labels.
    
    Parameters:
    - X: DataFrame containing the features.
    - y: DataFrame containing the target labels.
    
    Returns:
    - model: The trained RandomForest model.
    """
    print("Splitting data into training and testing sets...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training RandomForest model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train.values.ravel())
    
    # Evaluate the model
    print("Evaluating the model...")
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
    print("ROC AUC Score:", roc_auc_score(y_test, y_pred))
    
    return model

def save_model(model, file_path):
    """
    Saves the trained model to the specified file path.
    
    Parameters:
    - model: The trained machine learning model.
    - file_path: str, path to save the model (pickle file).
    """
    print(f"Saving the model to {file_path}")
    joblib.dump(model, file_path)

if __name__ == "__main__":
    # Get the absolute path to the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Step 1: Load the processed data
    X_file_path = os.path.join(project_root, "data", "processed", "X_processed.csv")
    y_file_path = os.path.join(project_root, "data", "processed", "y_processed.csv")
    X, y = load_processed_data(X_file_path, y_file_path)
    
    # Step 2: Train the model
    model = train_model(X, y)
    
    # Step 3: Save the trained model
    model_file_path = os.path.join(project_root, "models", "fraud_detection_model.pkl")
    save_model(model, model_file_path)
    
    print("Model training and saving pipeline completed successfully.")
