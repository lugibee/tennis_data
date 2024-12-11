import requests
import pandas as pd

# Define the API key and URLs
API_KEY = 'tBwblVyjQbqUzrf0SlrPU5pUl93ObsbDC9hFbTKJ'
COMPETITIONS_URL = f'https://api.sportradar.com/tennis/trial/v3/en/competitions.json?api_key={API_KEY}'
COMPLEXES_URL = f'https://api.sportradar.com/tennis/trial/v3/en/complexes.json?api_key={API_KEY}'
RANKINGS_URL = f'https://api.sportradar.com/tennis/trial/v3/en/double_competitors_rankings.json?api_key={API_KEY}'

# Define headers
HEADERS = {"accept": "application/json"}


def fetch_data(url):
    """Fetch data from the given URL."""
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
        print("Response content:", response.text)
        return None


def process_competitions(data):
    """Process competitions data."""
    categories = []
    competitions = []

    for competition in data['competitions']:
        category = competition['category']
        categories.append({
            'category_id': category['id'],
            'category_name': category['name']
        })
        competitions.append({
            'competition_id': competition['id'],
            'competition_name': competition['name'],
            'parent_id': competition.get('parent_id'),
            'type': competition['type'],
            'gender': competition['gender'],
            'category_id': category['id']
        })

    categories_df = pd.DataFrame(categories).drop_duplicates()
    competitions_df = pd.DataFrame(competitions)
    return categories_df, competitions_df


def process_complexes(data):
    """Process complexes data."""
    complexes = []
    venues = []

    for complex in data['complexes']:
        complexes.append({
            'complex_id': complex['id'],
            'complex_name': complex['name']
        })
        if 'venues' in complex:
            for venue in complex['venues']:
                venues.append({
                    'venue_id': venue['id'],
                    'venue_name': venue['name'],
                    'city_name': venue['city_name'],
                    'country_name': venue['country_name'],
                    'country_code': venue['country_code'],
                    'timezone': venue['timezone'],
                    'complex_id': complex['id']
                })

    complexes_df = pd.DataFrame(complexes).drop_duplicates()
    venues_df = pd.DataFrame(venues)
    return complexes_df, venues_df


def process_rankings(data):
    """Process rankings data."""
    competitors = []
    rankings = []

    for ranking in data['rankings']:
        for competitor_ranking in ranking['competitor_rankings']:
            competitor = competitor_ranking['competitor']
            competitors.append({
                'competitor_id': competitor['id'],
                'name': competitor['name'],
                'country': competitor['country'],
                'country_code': competitor.get('country_code'),
                'abbreviation': competitor['abbreviation']
            })
            rankings.append({
                'rank_id': competitor_ranking['rank'],
                'rank': competitor_ranking['rank'],
                'movement': competitor_ranking['movement'],
                'points': competitor_ranking['points'],
                'competitions_played': competitor_ranking['competitions_played'],
                'competitor_id': competitor['id']
            })

    competitors_df = pd.DataFrame(competitors).drop_duplicates()
    rankings_df = pd.DataFrame(rankings)
    return competitors_df, rankings_df


# Fetch and process data
competitions_data = fetch_data(COMPETITIONS_URL)
complexes_data = fetch_data(COMPLEXES_URL)
rankings_data = fetch_data(RANKINGS_URL)

if competitions_data:
    categories_df, competitions_df = process_competitions(competitions_data)
    categories_df.to_csv('categories.csv', index=False)
    competitions_df.to_csv('competitions.csv', index=False)

if complexes_data:
    complexes_df, venues_df = process_complexes(complexes_data)
    complexes_df.to_csv('complexes.csv', index=False)
    venues_df.to_csv('venues.csv', index=False)

if rankings_data:
    competitors_df, rankings_df = process_rankings(rankings_data)
    competitors_df.to_csv('competitors.csv', index=False)
    rankings_df.to_csv('rankings.csv', index=False)

print("Data has been saved to CSV files.")
