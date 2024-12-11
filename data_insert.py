import pandas as pd
import mysql.connector
from mysql.connector import Error

# Database connection details
db_config = {
    'host': 'sql12.freesqldatabase.com	',
    'user': 'sql12751178',
    'password': 'VPs6IEjTEL',
    'database': 'sql12751178'
}

# Define the cleaned CSV file paths
cleaned_csv_files = {
    #'Categories': 'cleaned_categories.csv',
    #'Competitions': 'cleaned_competitions.csv',
    #'Complexes': 'cleaned_complexes.csv',
    #'Venues': 'cleaned_venues.csv',
    #'Competitors': 'cleaned_competitors.csv',
    'Competitor_Rankings': 'cleaned_rankings.csv'
}

# Function to upload data to MySQL
def upload_to_mysql(table_name, df, connection):
    """Upload DataFrame to MySQL table."""
    cursor = connection.cursor()
    for _, row in df.iterrows():
        placeholders = ', '.join(['%s'] * len(row))
        columns = ', '.join(row.index)
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(sql, tuple(row))
    connection.commit()

try:
    # Establish the database connection
    connection = mysql.connector.connect(**db_config)
    if connection.is_connected():
        print("Connected to MySQL database")

        # Read and upload each cleaned CSV file to the corresponding MySQL table
        for table_name, file_path in cleaned_csv_files.items():
            df = pd.read_csv(file_path)
            upload_to_mysql(table_name, df, connection)
            print(f"Data from {file_path} uploaded to {table_name} table")

except Error as e:
    print(f"Error: {e}")
finally:
    if connection.is_connected():
        connection.close()
        print("MySQL connection closed")

print("Data upload completed.")
