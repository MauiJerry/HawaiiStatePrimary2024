import os
import pandas as pd

# Define the folder containing the CSV files
data_folder = './data'
output_folder = './output'

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# List all CSV files in the folder
csv_files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]

statewideSummaryName = "statewide summary.txt"
file_path = os.path.join(data_folder, statewideSummaryName)
print(file_path)
print(os.listdir(data_folder))

fd = os.open(file_path,)
line = os.read(fd,'r')
print(line)

# statewideDF = pd.read_csv(file_path)
# print("Statewide file =")
# print(statewideDF.describe())
# print("\nColumn names:")
# print(statewideDF.columns)
# print(statewideDF[0])

print("Processing complete.")
