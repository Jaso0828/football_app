import requests
from football.models import Club

API_KEY = 'a0f768f92194504083ab96f2b13e3466'
BASE_URL = 'https://v3.football.api-sports.io/'

def fetch_clubs(league_id: int, season: int):
    url = f'{BASE_URL}teams'
    headers = {'x-apisports-key': API_KEY}

    response = requests.get(url, headers=headers)
    
    print("Status code:", response.status_code)
    
    data = response.json()
    print("Raw JSON response:", data)  # <--- ovo će pokazati sve što API vraća

    if 'response' not in data or len(data['response']) == 0:
        print(f"Dohvaćeno 0 klubova za ligu {league_id}, sezonu {season}")
        return

    for item in data['response']:
        team = item['team']
        league_name = item['league']['name']
        
        print("Processing team:", team['name'])

        Club.objects.update_or_create(
            name=team['name'],
            defaults={
                'slug': team['name'].lower().replace(" ", "-"),
                'country': team['country'],
                'city': team.get('venue', ''),
                'league': league_name,
                'stadium': team.get('venue', ''),
                'logo_url': team['logo'],
                'is_active': True
            }
        )

    print(f"Dohvaćeno {len(data['response'])} klubova za ligu {league_id}, sezonu {season}")
