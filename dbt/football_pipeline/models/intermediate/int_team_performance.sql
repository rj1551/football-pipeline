WITH home_teams AS (
    SELECT
        match_id,
        utc_date,
        matchday,
        stage,
        season_id,
        home_team_id AS team_id,
        home_team_name AS team_name,
        home_team_tla AS team_tla,
        fulltime_home_goals AS fulltime_goals_scored,
        halftime_home_goals AS halftime_goals_scored,
        fulltime_away_goals AS fulltime_goals_conceded,
        halftime_away_goals AS halftime_goals_conceded,
        CASE
            WHEN winner = 'HOME_TEAM' THEN 'WIN'
            WHEN winner = 'DRAW' THEN 'DRAW'
            ELSE 'LOSE'
        END AS result,
        duration,
        TRUE AS is_home
    FROM
        {{ ref('stg_matches') }}
)
, away_teams AS (
    SELECT
        match_id,
        utc_date,
        matchday,
        stage,
        season_id,
        away_team_id AS team_id,
        away_team_name AS team_name,
        away_team_tla AS team_tla,
        fulltime_away_goals AS fulltime_goals_scored,
        halftime_away_goals AS halftime_goals_scored,
        fulltime_home_goals AS fulltime_goals_conceded,
        halftime_home_goals AS halftime_goals_conceded,
        CASE
            WHEN winner = 'AWAY_TEAM' THEN 'WIN'
            WHEN winner = 'DRAW' THEN 'DRAW'
            ELSE 'LOSE'
        END AS result,
        duration,
        FALSE AS is_home
    FROM
        {{ ref('stg_matches') }}
)
SELECT
    match_id,
    utc_date,
    matchday,
    stage,
    season_id,
    team_id,
    team_name,
    team_tla,
    fulltime_goals_scored,
    halftime_goals_scored,
    fulltime_goals_conceded,
    halftime_goals_conceded,
    result,
    duration,
    is_home
FROM
    home_teams
UNION ALL
SELECT
    * -- same columns as above from home_teams
FROM    
    away_teams