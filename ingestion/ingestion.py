import requests
import json
import os
from dotenv import load_dotenv
import duckdb
from pathlib import Path
from datetime import datetime

load_dotenv()
football_data_key = os.getenv('FOOTBALL_DATA_KEY')


# Get the directory of the current file using pathlib
script_dir = Path(__file__).parent.absolute()
con = duckdb.connect(script_dir.parent / 'data' / 'football_db.duckdb')
con.sql("""
CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY,
    match_data JSON,
    ingested_at TIMESTAMP
)""")

# matches
uri = 'https://api.football-data.org/v4/competitions/PL/matches?season=2025'
headers = { 'X-Auth-Token':  football_data_key}

matches_ingestion_time = datetime.now()
response = requests.get(uri, headers=headers)

with open(script_dir.parent / 'data' / 'raw' / 'matches.json', "w") as file:
    json.dump(response.json()['matches'], file, indent=4)

con.execute(f"""
INSERT OR IGNORE INTO 
    matches
SELECT
    id, to_json(match_data), $1
FROM
    '{(script_dir.parent / 'data' / 'raw' / 'matches.json').as_posix()}' AS match_data
WHERE
    status = 'FINISHED'
""", [matches_ingestion_time]) # insert if not exists

# scorers
uri = 'https://api.football-data.org/v4/competitions/PL/scorers?season=2025'
headers = { 'X-Auth-Token':  football_data_key}

scorers_ingestion_time = datetime.now()
response = requests.get(uri, headers=headers)

response_json = response.json()
season_obj = response_json['season']
scorers_obj = response_json['scorers']
with open(script_dir.parent / 'data' / 'raw' / 'scorers.json', "w") as file:
    json.dump([scorer | {'season_id':season_obj['id']} for scorer in scorers_obj], file, indent=4)


con.sql("""
CREATE TABLE IF NOT EXISTS scorers (
    id INTEGER,
    season_id INTEGER,
    scorer_data JSON,
    ingested_at TIMESTAMP,
    PRIMARY KEY (id, season_id)
)""")

con.execute(f"""
INSERT INTO 
    scorers (id, season_id, scorer_data, ingested_at)
SELECT
    (scorer_data::JSON->>'$.player.id')::INTEGER, (scorer_data::JSON->>'$.season_id')::INTEGER, to_json(scorer_data), $1
FROM
    '{(script_dir.parent / 'data' / 'raw' / 'scorers.json').as_posix()}' AS scorer_data
ON CONFLICT DO UPDATE SET
    scorer_data = EXCLUDED.scorer_data,
    ingested_at = EXCLUDED.ingested_at
""", [scorers_ingestion_time]) #upsert

# print(response.json())
print(con.sql('SELECT COUNT(*) FROM scorers'))
print(con.sql('SELECT DISTINCT ingested_at FROM scorers'))