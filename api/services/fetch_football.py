import requests
from football.models import Club, Stadium
from django.conf import settings


API_KEY = settings.API_FOOTBALL_KEY
BASE_URL = 'https://v3.football.api-sports.io/'

def fetch_clubs(league_id: int, season: int):
    url = f'{BASE_URL}teams'
    headers = {'x-apisports-key': API_KEY}
    params = {'league': league_id, 'season': season}

    response = requests.get(url, headers=headers, params=params)
    
    print("Status code:", response.status_code)
    
    data = response.json()
    print("Raw JSON response:", data)  # <--- ovo će pokazati sve što API vraća

    if 'response' not in data or len(data['response']) == 0:
        print(f"Dohvaćeno 0 klubova za ligu {league_id}, sezonu {season}")
        return

    for item in data['response']:
        team = item['team']
        venue = item.get('venue', {})
        
        print("Processing team:", team['name'])

        stadium, _ = Stadium.objects.update_or_create(
            name=venue['name'],
            defaults={
            'address': venue.get('address', ''),
            'city': venue.get('city', ''),
            'capacity': venue.get('capacity', None),
            'surface': venue.get('surface', ''),
            'image_url': venue.get('image', ''),
        }
    )

        Club.objects.update_or_create(
            name=team['name'],
            defaults={
                'slug': team['name'].lower().replace(" ", "-"),
                'country': team.get('country', 'Unknown'),
                'city': venue.get('city', ''),
                'league': 'Premier League',
                'stadium': stadium,
                'logo_url': team.get('logo', ''),
                'founding_year': team.get('founded'),
                'is_active': True
    }
)


    print(f"Dohvaćeno {len(data['response'])} klubova za ligu {league_id}, sezonu {season}")
