import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error

# Database connection details
db_config = {
    'host': 'sql12.freesqldatabase.com',
    'user': 'sql12751178',
    'password': 'VPs6IEjTEL',  # Replace with your actual password
    'database': 'sql12751178'
}

# Function to execute SQL query and return DataFrame
def execute_query(query):
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            df = pd.read_sql(query, connection)
            return df
    except Error as e:
        st.error(f"Error: {e}")
    finally:
        if connection.is_connected():
            connection.close()

# Streamlit UI
st.title("Game Analytics: Unlocking Tennis Data with SportRadar API")

# Sidebar for navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio("Go to", ["Event Exploration", "Trend Analysis", "Performance Insights", "Decision Support"])

if options == "Event Exploration":
    st.header("Event Exploration")
    
    # 1. List all competitions along with their category name
    query = """
    SELECT c.competition_name, cat.category_name
    FROM Competitions c
    JOIN Categories cat ON c.category_id = cat.category_id
    """
    df = execute_query(query)
    st.dataframe(df)

    # 2. Count the number of competitions in each category
    query = """
    SELECT cat.category_name, COUNT(*) as competition_count
    FROM Competitions c
    JOIN Categories cat ON c.category_id = cat.category_id
    GROUP BY cat.category_name
    """
    df = execute_query(query)
    st.bar_chart(df.set_index('category_name'))

    # 3. Find all competitions of type 'doubles'
    query = "SELECT * FROM Competitions WHERE type = 'doubles'"
    df = execute_query(query)
    st.dataframe(df)

    # 4. Get competitions that belong to a specific category (e.g., ITF Men)
    category = st.text_input("Enter category name (e.g., ITF Men):")
    if category:
        query = f"""
        SELECT competition_id,competition_name ,category_name FROM Competitions c
        JOIN Categories cat ON c.category_id = cat.category_id
        WHERE cat.category_name = '{category}'
        """
        df = execute_query(query)
        st.dataframe(df)

    # 5. Identify parent competitions and their sub-competitions
    query = """
    SELECT parent.competition_name as parent_competition, child.competition_name as sub_competition
    FROM Competitions parent
    JOIN Competitions child ON parent.competition_id = child.parent_id
    """
    df = execute_query(query)
    st.dataframe(df)

    # 6. Analyze the distribution of competition types by category
    query = """
    SELECT cat.category_name, c.type, COUNT(*) as type_count
    FROM Competitions c
    JOIN Categories cat ON c.category_id = cat.category_id
    GROUP BY cat.category_name, c.type
    """
    df = execute_query(query)
    st.write(" Analyze the distribution of competition types by category")
    st.write(df)  # Print the DataFrame to check its content
    if 'category_name' in df.columns and 'type' in df.columns:
        st.bar_chart(df.set_index(['category_name', 'type']))
    else:
        st.error("The DataFrame does not contain the required columns: 'category_name' and 'type'")

    # 7. List all competitions with no parent (top-level competitions)
    #--query = "SELECT * FROM Competitions WHERE parent_id IS NULL"
    #--df = execute_query(query)
    #--st.dataframe(df)

elif options == "Trend Analysis":
    st.header("Trend Analysis")
    
    # 8. List all venues along with their associated complex name
    query = """
    SELECT v.venue_name, c.complex_name
    FROM Venues v
    JOIN Complexes c ON v.complex_id = c.complex_id
    """
    df = execute_query(query)
    st.dataframe(df)

    # 9. Count the number of venues in each complex
    query = """
    SELECT c.complex_name, COUNT(*) as venue_count
    FROM Venues v
    JOIN Complexes c ON v.complex_id = c.complex_id
    GROUP BY c.complex_name
    """
    df = execute_query(query)
    st.bar_chart(df.set_index('complex_name'))

    # 10. Get details of venues in a specific country (e.g., Chile)
    country = st.text_input("Enter country name (e.g., Chile):")
    if country:
        query = f"SELECT * FROM Venues WHERE country_name = '{country}'"
        df = execute_query(query)
        st.dataframe(df)

    # 11. Identify all venues and their timezones
    query = "SELECT venue_name, timezone FROM Venues"
    df = execute_query(query)
    st.dataframe(df)

    # 12. Find complexes that have more than one venue
    query = """
    SELECT c.complex_name, COUNT(*) as venue_count
    FROM Venues v
    JOIN Complexes c ON v.complex_id = c.complex_id
    GROUP BY c.complex_name
    HAVING venue_count > 1
    """
    df = execute_query(query)
    st.dataframe(df)

    # 13. List venues grouped by country
    query = """
    SELECT country_name, COUNT(*) as venue_count
    FROM Venues
    GROUP BY country_name
    """
    df = execute_query(query)
    st.bar_chart(df.set_index('country_name'))

    # 14. Find all venues for a specific complex (e.g., Nacional)
    complex_name = st.text_input("Enter complex name (e.g., Nacional):")
    if complex_name:
        query = f"""
        SELECT  'complex_name','c.complex_id', 'venue_name', 'city_name', 'country_name', 'country_code', 'timezone' FROM Venues v
        JOIN Complexes c ON v.complex_id = c.complex_id
        WHERE c.complex_name = '{complex_name}'
        """
        df = execute_query(query)
        st.dataframe(df)

elif options == "Performance Insights":
    st.header("Performance Insights")
    
    # 15. Get all competitors with their rank and points
    query = """
    SELECT comp.name, rank.rank, rank.points
    FROM Competitors comp
    left JOIN Competitor_Rankings rank ON comp.competitor_id = rank.competitor_id
    """
    df = execute_query(query)
    st.dataframe(df)

    # 16. Find competitors ranked in the top 5
    query = """
    SELECT comp.name, rank.rank, rank.points
    FROM Competitors comp
    JOIN Competitor_Rankings rank ON comp.competitor_id = rank.competitor_id
    WHERE rank.rank <= 5
    """
    df = execute_query(query)
    st.dataframe(df)

    # 17. List competitors with no rank movement (stable rank)
    query = """
    SELECT comp.name, rank.rank, rank.points
    FROM Competitors comp
    JOIN Competitor_Rankings rank ON comp.competitor_id = rank.competitor_id
    WHERE rank.movement = 0
    """
    df = execute_query(query)
    st.dataframe(df)

    # 18. Get the total points of competitors from a specific country (e.g., Croatia)
    country = st.text_input("Enter country name (e.g., Croatia):")
    if country:
        query = f"""
        SELECT SUM(rank.points) as total_points
        FROM Competitors comp
        JOIN Competitor_Rankings rank ON comp.competitor_id = rank.competitor_id
        WHERE comp.country = '{country}'
        """
        df = execute_query(query)
        st.dataframe(df)

    # 19. Count the number of competitors per country
    query = """
    SELECT comp.country, COUNT(*) as competitor_count
    FROM Competitors comp
    GROUP BY comp.country
    """
    df = execute_query(query)
    st.bar_chart(df.set_index('country'))

    # 20. Find competitors with the highest points in the current week
    query = """
    SELECT comp.name, rank.points
    FROM Competitors comp
    JOIN Competitor_Rankings rank ON comp.competitor_id = rank.competitor_id
    ORDER BY rank.points DESC
    LIMIT 1
    """
    df = execute_query(query)
    st.dataframe(df)S

elif options == "Decision Support":
    st.header("Decision Support")
    st.write("This section can be used to provide data-driven insights to event organizers or sports bodies for resource allocation.")
    # Add more decision support queries and visualizations as needed

st.sidebar.info("Use the navigation menu to explore different sections of the application.")