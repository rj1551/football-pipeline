SELECT 
    match_id, 
    utc_date,
    matchday,
    stage,
    season_id,
    home_team_id,
    away_team_id,
    fulltime_home_goals,
    fulltime_away_goals,
    halftime_home_goals,
    halftime_away_goals,
    winner,
    duration
FROM
    {{ ref('stg_matches') }}