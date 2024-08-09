import os
import pandas as pd

# Define the folder containing the CSV files
data_folder = './data'
output_folder = './output'

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# List all CSV files in the folder
csv_files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]

# Process each CSV file separately
for file in csv_files:
    file_path = os.path.join(data_folder, file)
    df = pd.read_csv(file_path)

    # Perform some basic analysis on the DataFrame
    print(f"Processing file: {file}")
    print("Summary statistics:")
    print(df.describe())

    print("\nColumn names:")
    print(df.columns)

    # Example analysis: Group by a specific column and calculate the mean
    if 'column_name' in df.columns:
        grouped_df = df.groupby('column_name').mean()
        print(f"\nGrouped by 'column_name' for {file}:")
        print(grouped_df)

    # Example analysis: Filter rows based on a condition
    if 'another_column' in df.columns:
        filtered_df = df[df['another_column'] > 50]
        print(f"\nFiltered rows where 'another_column' > 50 for {file}:")
        print(filtered_df)

        # Save the filtered data to a new CSV file
        output_csv_path = os.path.join(output_folder, f'filtered_{file}')
        filtered_df.to_csv(output_csv_path, index=False)
        print(f"\nFiltered data saved to {output_csv_path}")

    print("\n" + "-" * 50 + "\n")

print("Processing complete.")
