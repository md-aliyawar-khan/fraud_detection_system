import os
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
import joblib

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
    
    # Check if files exist
    if not os.path.exists(X_file_path):
        raise FileNotFoundError(f"Error: The file {X_file_path} does not exist. Please check the path.")
    if not os.path.exists(y_file_path):
        raise FileNotFoundError(f"Error: The file {y_file_path} does not exist. Please check the path.")
    
    try:
        X = pd.read_csv(X_file_path)
        y = pd.read_csv(y_file_path)
    except Exception as e:
        print(f"An error occurred while loading the files: {e}")
        raise
    
    return X, y

def tune_hyperparameters(X, y):
    """
    Tune hyperparameters of a RandomForest model using GridSearchCV.
    
    Parameters:
    - X: DataFrame containing the features.
    - y: DataFrame containing the target labels.
    
    Returns:
    - best_model: The RandomForest model with the best hyperparameters.
    """
    print("Splitting data into training and testing sets...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Define the hyperparameter grid
    param_grid = {
        'n_estimators': [100, 200, 300],         # Number of trees
        'max_depth': [None, 10, 20, 30],         # Max depth of each tree
        'min_samples_split': [2, 5, 10],         # Minimum samples required to split an internal node
        'min_samples_leaf': [1, 2, 4],           # Minimum number of samples required to be a leaf node
    }

    # Initialize the RandomForest model
    rf = RandomForestClassifier(random_state=42)
    
    # Initialize GridSearchCV
    grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, scoring='roc_auc', verbose=2, n_jobs=-1)
    
    # Fit the grid search to the data
    print("Tuning hyperparameters...")
    grid_search.fit(X_train, y_train)
    
    # Best hyperparameters
    print("Best hyperparameters found: ", grid_search.best_params_)
    
    # Best model
    best_model = grid_search.best_estimator_
    
    # Evaluate the model on the test data
    print("Evaluating the best model on the test data...")
    y_pred = best_model.predict(X_test)
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    print("ROC AUC Score:", roc_auc_score(y_test, y_pred))
    
    return best_model

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
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Step 1: Load the processed data
    X_file_path = os.path.join(project_root, "data", "processed", "X_processed.csv")
    y_file_path = os.path.join(project_root, "data", "processed", "y_processed.csv")
    X, y = load_processed_data(X_file_path, y_file_path)
    
    # Step 2: Tune the hyperparameters
    best_model = tune_hyperparameters(X, y)
    
    # Step 3: Save the best model
    model_file_path = os.path.join(project_root, "models", "best_fraud_detection_model.pkl")
    save_model(best_model, model_file_path)
    
    print("Hyperparameter tuning and model saving completed successfully.")
