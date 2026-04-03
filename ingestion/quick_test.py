import duckdb
from pathlib import Path

script_dir = Path(__file__).parent.absolute()
con = duckdb.connect(script_dir.parent / 'data' / 'football_db.duckdb')

print(con.sql('SELECT * FROM stg_matches'))