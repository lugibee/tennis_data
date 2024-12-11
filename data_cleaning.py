import pandas as pd

# Define the CSV file paths
csv_files = {
    'categories': 'categories.csv',
    'competitions': 'competitions.csv',
    'complexes': 'complexes.csv',
    'venues': 'venues.csv',
    'competitors': 'competitors.csv',
    'rankings': 'rankings.csv'
}

# Function to clean data
def clean_data(df):
    """Remove null values and duplicates from the DataFrame."""
    df = df.dropna()  # Remove rows with null values
    df = df.drop_duplicates()  # Remove duplicate rows
    return df

# Read, clean, and save each CSV file
for name, file_path in csv_files.items():

    df = pd.read_csv(file_path)
    if name =='cleaned_rankings':
            df["competitor_id"]=df["competitor_id"].str.split(":").str[-1]
        
    cleaned_df = clean_data(df)
    cleaned_df.to_csv(f'cleaned_{file_path}', index=False)
    print(f"Cleaned data saved to cleaned_{file_path}")

print("Data cleaning completed.")
