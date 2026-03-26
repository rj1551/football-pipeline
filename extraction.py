import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# uri = 'https://api.football-data.org/v4/matches/330299'
# uri = 'https://api.football-data.org/v4/competitions/PL/scorers'
uri = 'https://api.football-data.org/v4/persons/8133/matches'
football_data_key = os.getenv('FOOTBALL_DATA_KEY')
headers = { 'X-Auth-Token':  football_data_key}

response = requests.get(uri, headers=headers)
# for match in response.json()['matches']:
#     print(match)

print(response.json())