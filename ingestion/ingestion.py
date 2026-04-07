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
with duckdb.connect(script_dir.parent / 'data' / 'football_db.duckdb') as con:
    con.sql("""
    CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY,
        match_data JSON,
        ingested_at TIMESTAMP
    )""")

    # matches
    matches_uri = 'https://api.football-data.org/v4/competitions/PL/matches?season=2025'
    headers = { 'X-Auth-Token':  football_data_key}

    matches_ingestion_time = datetime.now()
    matches_response = requests.get(matches_uri, headers=headers)

    matches_data = matches_response.json()['matches']
    with open(script_dir.parent / 'data' / 'raw' / 'matches.json', "w") as file:
        json.dump(matches_data, file, indent=4)

    con.execute(f"""
    INSERT OR IGNORE INTO 
        matches (id, match_data, ingested_at)
    SELECT
        id, 
        to_json(match_data), 
        $1
    FROM
        '{(script_dir.parent / 'data' / 'raw' / 'matches.json').as_posix()}' AS match_data
    WHERE
        status = 'FINISHED'
    """, [matches_ingestion_time]) # insert if not exists

    response_ids = set(m['id'] for m in matches_data if m['status']=='FINISHED')
    table_ids = set(row[0] for row in con.sql("SELECT id FROM matches").fetchall())
    missing = response_ids - table_ids
    if missing:
        raise ValueError(f"Matches load validation failed: {len(missing)} match IDs missing from DB:\n{missing}")

    # scorers
    scorers_uri = 'https://api.football-data.org/v4/competitions/PL/scorers?season=2025'

    scorers_ingestion_time = datetime.now()
    scorers_response = requests.get(scorers_uri, headers=headers)

    scorers_response_json = scorers_response.json()
    season_data = scorers_response_json['season']
    scorers_data = scorers_response_json['scorers']
    with open(script_dir.parent / 'data' / 'raw' / 'scorers.json', "w") as file:
        json.dump([scorer | {'season_id':season_data['id']} for scorer in scorers_data], file, indent=4)


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
        (scorer_data::JSON->>'$.player.id')::INTEGER, 
        (scorer_data::JSON->>'$.season_id')::INTEGER, 
        to_json(scorer_data), $1
    FROM
        '{(script_dir.parent / 'data' / 'raw' / 'scorers.json').as_posix()}' AS scorer_data
    ON CONFLICT DO UPDATE SET
        scorer_data = EXCLUDED.scorer_data,
        ingested_at = EXCLUDED.ingested_at
    """, [scorers_ingestion_time]) #upsert


    response_ids = set((s['player']['id'], season_data['id']) for s in scorers_data)
    table_ids = set((row[0], row[1]) for row in con.sql("SELECT id, season_id FROM scorers").fetchall())
    missing = response_ids - table_ids
    if missing:
        raise ValueError(f"Scorers load validation failed: {len(missing)} match IDs missing from DB:\n{missing}")



# print(response.json())
# print(con.sql('SELECT COUNT(*) FROM scorers'))
# print(con.sql('SELECT DISTINCT ingested_at FROM scorers'))
# print(con.sql('SELECT * FROM stg_scorers WHERE assists IS NULL OR penalties IS NULL'))

# print(con.sql('''SELECT 
#     scorer_data->>'$.penalties' AS raw_val,
#     (scorer_data->>'$.penalties')::INTEGER AS casted_val,
#     COALESCE((scorer_data->>'$.penalties')::INTEGER, 0) AS coalesced
# FROM scorers
# WHERE (scorer_data::JSON->>'$.player.id')::INTEGER=11777'''))