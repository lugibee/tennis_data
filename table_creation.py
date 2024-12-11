import mysql.connector
from mysql.connector import Error

# Database connection details
db_config = {
    'host': 'sql12.freesqldatabase.com	',
    'user': 'sql12751178',
    'password': 'VPs6IEjTEL',
    'database': 'sql12751178'
}

# SQL statements to create tables
create_tables_sql = [
    """
    CREATE TABLE IF NOT EXISTS Categories (
        category_id VARCHAR(50) PRIMARY KEY,
        category_name VARCHAR(100) NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Competitions (
        competition_id VARCHAR(50) PRIMARY KEY,
        competition_name VARCHAR(100) NOT NULL,
        parent_id VARCHAR(50),
        type VARCHAR(20) NOT NULL,
        gender VARCHAR(10) NOT NULL,
        category_id VARCHAR(50),
        FOREIGN KEY (category_id) REFERENCES Categories(category_id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Complexes (
        complex_id VARCHAR(50) PRIMARY KEY,
        complex_name VARCHAR(100) NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Venues (
        venue_id VARCHAR(50) PRIMARY KEY,
        venue_name VARCHAR(100) NOT NULL,
        city_name VARCHAR(100) NOT NULL,
        country_name VARCHAR(100) NOT NULL,
        country_code CHAR(3) NOT NULL,
        timezone VARCHAR(100) NOT NULL,
        complex_id VARCHAR(50),
        FOREIGN KEY (complex_id) REFERENCES Complexes(complex_id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Competitors (
        competitor_id VARCHAR(50) PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        country VARCHAR(100) NOT NULL,
        country_code CHAR(3) NOT NULL,
        abbreviation VARCHAR(10) NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Competitor_Rankings (
        rank_id SERIAL PRIMARY KEY,
        rank INT NOT NULL,
        movement INT NOT NULL,
        points INT NOT NULL,
        competitions_played INT NOT NULL,
        competitor_id VARCHAR(50),
        FOREIGN KEY (competitor_id) REFERENCES Competitors(competitor_id)
    );
    """
]

try:
    # Establish the database connection
    connection = mysql.connector.connect(**db_config)
    if connection.is_connected():
        print("Connected to MySQL database")

        cursor = connection.cursor()
        # Execute each SQL statement to create the tables
        for sql in create_tables_sql:
            cursor.execute(sql)
            print("Table created successfully")

        connection.commit()

except Error as e:
    print(f"Error: {e}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection closed")

print("Tables creation completed.")
