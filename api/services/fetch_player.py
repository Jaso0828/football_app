import requests
import time
from football.models import Player, Club
from django.conf import settings

API_KEY = settings.API_FOOTBALL_KEY
BASE_URL = 'https://v3.football.api-sports.io/'


def call_api(endpoint: str, params: dict):
    """
    Generička funkcija za pozivanje API-ja
    
    Args:
        endpoint: API endpoint (npr. 'players', 'teams')
        params: Dictionary s parametrima
    
    Returns:
        JSON response ili None ako greška
    """
    url = f'{BASE_URL}{endpoint}'
    headers = {'x-apisports-key': API_KEY}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        print(f'Status code: {response.status_code} | Endpoint: {endpoint} | Params: {params}')
        
        if response.status_code == 429:
            print("⚠️  Rate limit dostignut! Čekam 60 sekundi...")
            time.sleep(60)
            return call_api(endpoint, params)  # Retry
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Greška: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None


def fetch_all_players_paginated_by_team(team_id: int, season: int, page: int = 1, all_players: list = None):
    """
    Rekurzivno dohvaća sve igrače tima s paginacijom
    
    Args:
        team_id: ID tima (npr. 49 za Chelsea)
        season: Sezona (npr. 2024)
        page: Trenutna stranica (default 1)
        all_players: Lista svih igrača (za rekurziju)
    
    Returns:
        Lista svih igrača
    """
    if all_players is None:
        all_players = []
    
    params = {
        'team': team_id,
        'season': season,
        'page': page
    }
    
    data = call_api('players', params)
    
    if not data or 'response' not in data:
        return all_players
    
    # Dodaj igrače s trenutne stranice
    all_players.extend(data['response'])
    
    # Provjeri paging info
    paging = data.get('paging', {})
    current_page = paging.get('current', page)
    total_pages = paging.get('total', 1)
    
    print(f"   📄 Stranica {current_page}/{total_pages} | Igrača: {len(data['response'])}")
    
    # Ako ima još stranica, pozovi rekurzivno
    if current_page < total_pages:
        time.sleep(1)  # Delay između poziva
        return fetch_all_players_paginated_by_team(team_id, season, page + 1, all_players)
    
    return all_players


def save_players_to_db(players_data: list):
    """
    Sprema igrače u bazu podataka
    
    Args:
        players_data: Lista igrača iz API-ja
    """
    saved_count = 0
    skipped_count = 0
    
    for item in players_data:
        player_data = item['player']
        stats = item['statistics'][0] if item['statistics'] else {}
        
        # Dohvati ime tima
        team_name = stats.get('team', {}).get('name')
        
        if not team_name:
            print(f"⚠️  Preskaćem {player_data['name']} - nema tima")
            skipped_count += 1
            continue
        
        try:
            club = Club.objects.get(name=team_name)
        except Club.DoesNotExist:
            print(f"⚠️  Klub '{team_name}' ne postoji u bazi!")
            skipped_count += 1
            continue
        
        # Spremi igrača
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
        saved_count += 1
    
    print(f"   ✅ Spremljeno: {saved_count} | ⚠️  Preskočeno: {skipped_count}")


def fetch_premier_league_players_by_teams(season: int = 2024):
    """
    Dohvaća igrače za sve Premier League timove (pristup po team_id)
    
    Args:
        season: Sezona (default 2024)
    """
    premier_league_teams = {
        'Arsenal': 42,
        'Aston Villa': 66,
        'Bournemouth': 35,
        'Brentford': 55,
        'Brighton': 51,
        'Chelsea': 49,
        'Crystal Palace': 52,
        'Everton': 45,
        'Fulham': 36,
        'Ipswich': 57,
        'Leicester': 46,
        'Liverpool': 40,
        'Manchester City': 50,
        'Manchester United': 33,
        'Newcastle': 34,
        'Nottingham Forest': 65,
        'Southampton': 41,
        'Tottenham': 47,
        'West Ham': 48,
        'Wolves': 39,
    }
    
    total_players = 0
    
    print(f"\n{'='*60}")
    print(f"🏆 PREMIER LEAGUE PLAYERS - SEZONA {season}")
    print(f"{'='*60}\n")
    
    for idx, (team_name, team_id) in enumerate(premier_league_teams.items(), 1):
        print(f"\n{'='*60}")
        print(f"[{idx}/{len(premier_league_teams)}] 🔄 {team_name} (ID: {team_id})")
        print(f"{'='*60}")
        
        # Dohvati sve stranice za tim
        players_data = fetch_all_players_paginated_by_team(team_id, season)
        
        if players_data:
            save_players_to_db(players_data)
            total_players += len(players_data)
        else:
            print(f"   ⚠️  Nema podataka za {team_name}")
        
        # Rate limit protection (2 sekunde između timova)
        if idx < len(premier_league_teams):
            print(f"   ⏳ Čekam 2 sekunde...")
            time.sleep(2)
    
    print(f"\n{'='*60}")
    print(f"✅ ZAVRŠENO!")
    print(f"📊 Ukupno dohvaćeno: {total_players} igrača")
    print(f"{'='*60}\n")
    
    # Ispis statistike po klubovima
    from django.db.models import Count
    clubs = Player.objects.values('club__name').annotate(count=Count('id')).order_by('-count')
    
    print(f"\n{'='*60}")
    print(f"📊 STATISTIKA PO KLUBOVIMA")
    print(f"{'='*60}")
    for club in clubs:
        print(f"{club['club__name']}: {club['count']} igrača")
    print(f"{'='*60}\n")