import pandas as pd
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE

def load_data(file_path):
    """
    Loads the dataset from the specified file path.
    
    Parameters:
    - file_path: str, path to the dataset (CSV file).
    
    Returns:
    - DataFrame containing the dataset.
    """
    print(f"Loading data from {file_path}")
    data = pd.read_csv(file_path)
    return data

def preprocess_data(data):
    """
    Preprocess the data by scaling the 'Amount' column and applying SMOTE for class imbalance.
    
    Parameters:
    - data: DataFrame containing the raw data.
    
    Returns:
    - X_resampled: The features after resampling using SMOTE.
    - y_resampled: The target labels after resampling.
    - scaler: The fitted StandardScaler for later use.
    """
    print("Starting data preprocessing...")

    # Normalizing the 'Amount' column
    scaler = StandardScaler()
    data['Amount'] = scaler.fit_transform(data['Amount'].values.reshape(-1, 1))
    
    # Splitting the features (X) and target (y)
    X = data.drop('Class', axis=1)
    y = data['Class']
    
    # Apply SMOTE to handle class imbalance
    print("Applying SMOTE to handle class imbalance...")
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)
    
    print("Data preprocessing complete.")
    return X_resampled, y_resampled, scaler

def save_processed_data(X, y, X_file_path, y_file_path):
    """
    Saves the processed features and labels to the specified file paths.
    
    Parameters:
    - X: Processed features.
    - y: Processed labels.
    - X_file_path: str, path to save the features.
    - y_file_path: str, path to save the labels.
    """
    print(f"Saving processed data to {X_file_path} and {y_file_path}")
    pd.DataFrame(X).to_csv(X_file_path, index=False)
    pd.DataFrame(y, columns=['Class']).to_csv(y_file_path, index=False)

if __name__ == "__main__":
    # Step 1: Load the raw data using the absolute path
    import os
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(project_root, "data", "raw", "creditcard_2023.csv")
    data = load_data(file_path)
    
    # Step 2: Preprocess the data
    X_resampled, y_resampled, scaler = preprocess_data(data)
    
    # Step 3: Save the processed data to the 'data/processed/' folder
    X_processed_path = "data/processed/X_processed.csv"
    y_processed_path = "data/processed/y_processed.csv"
    save_processed_data(X_resampled, y_resampled, X_processed_path, y_processed_path)
    
    # Step 4: Save the scaler for later use in the API
    import joblib
    import os
    scaler_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models", "scaler.pkl")
    joblib.dump(scaler, scaler_path)
    print(f"Scaler saved to {scaler_path}")

    print("Data preprocessing pipeline completed successfully.")
