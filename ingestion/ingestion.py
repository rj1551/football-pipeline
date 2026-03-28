import requests
import json
import os
from dotenv import load_dotenv
import duckdb
from pathlib import Path
from datetime import datetime

load_dotenv()

from pathlib import Path
# Get the directory of the current file using pathlib
script_dir = Path(__file__).parent.absolute()
con = duckdb.connect(script_dir.parent / 'data' / 'football_db.duckdb')
con.sql("""
CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY,
    match_data JSON,
    ingested_at TIMESTAMP
)""")


uri = 'https://api.football-data.org/v4/competitions/PL/matches?season=2025'
football_data_key = os.getenv('FOOTBALL_DATA_KEY')
headers = { 'X-Auth-Token':  football_data_key}

ingestion_time = datetime.now()
response = requests.get(uri, headers=headers)

with open(script_dir.parent / 'data' / 'raw' / 'matches.json', "w") as file:
    json.dump(response.json()['matches'], file, indent=4)
print(len(response.json()['matches']))

con.execute(f"""
INSERT OR IGNORE INTO 
    matches
SELECT
    id, to_json(match_data), $1
FROM
    '{(script_dir.parent / 'data' / 'raw' / 'matches.json').as_posix()}' AS match_data
WHERE
    status = 'FINISHED'
""", [ingestion_time]) # insert if not exists