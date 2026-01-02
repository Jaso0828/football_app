import requests
from football.models import Player, Club
from django.conf import settings

API_KEY = settings.API_FOOTBALL_KEY
BASE_URL = 'https://v3.football.api-sports.io/'

def fetch_players(team_id: int, season_id: int):
    URL = f'{BASE_URL}players'
    headers = {'x-apisports-key': API_KEY}
    params = {'team': team_id, 'season': season_id}

    response = requests.get(URL, headers=headers ,params=params)
    print(f'Status code: {response.status_code}')

    data = response.json()

    if 'response' not in data or len(data['response']) == 0:
        print(f'Nema igraca za tim {team_id}, sezona {season_id}')
        return
    
    team_name = data['response'][0]['statistics'][0]['team']['name'] 

    try:
        club = Club.objects.get(name=team_name)
    except Club.DoesNotExist:
        print(f"Klub '{team_name}' ne postoji u bazi! Prvo dohvati klubove.")
        return
    
    for item in data['response']:
        player_data = item['player']
        stats = item['statistics'][0] if item['statistics'] else {}

    Player.objects.update_or_create(
        name=player_data['name'],
        club=club,
        defaults={
        'age': player_data.get('age'),
        'nationality': player_data.get('nationality', 'Unknown'),
        'position': stats.get('games', {}).get('position', 'Unknown'),
        'number': stats.get('games', {}).get('number'),
        'photo_url': player_data.get('photo', ''),
        'birth_date': player_data.get('birth', {}).get('date'),
        'height': player_data.get('height'),
        'weight': player_data.get('weight'),
        }
    )

def fetch_all_premier_league_players(season: int = 2024):
    premier_league_teams = {
        'Arsenal': 42,
        'Aston Villa': 66,
        'Chelsea': 49,
        'Liverpool': 40,
        'Manchester City': 50,
        'Manchester United': 33,
        'Newcastle': 34,
        'Tottenham': 47,
        'Brighton': 51,
        'Fulham': 36,
        'Brentford': 55,
        'Crystal Palace': 52,
        'Everton': 45,
        'Leicester': 46,
        'Nottingham Forest': 65,
        'West Ham': 48,
        'Wolves': 39,
        'Bournemouth': 35,
        'Luton': 163,
        'Burnley': 44,
    }
    
    for team_name, team_id in premier_league_teams.items():
        print(f"\n{'='*50}")
        print(f"Dohvaćam igrače za {team_name}...")
        print(f"{'='*50}")
        fetch_players(team_id, season)