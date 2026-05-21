import pandas as pd

# Define the path to the dataset
file_path = r'C:\Users\aliya\Desktop\fraud_detection_project\data\raw\creditcard_2023.csv'

# Load the dataset into a pandas DataFrame
data = pd.read_csv(file_path)

# Display the first few rows of the dataset
print(data.head())

# Display basic info about the dataset
print(data.info())