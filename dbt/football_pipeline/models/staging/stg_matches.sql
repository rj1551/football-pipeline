SELECT 
    id AS match_id, 
    (match_data->>'$.utcDate')::TIMESTAMP AS utc_date,
    (match_data->>'$.matchday')::INTEGER AS matchday,
    match_data->>'$.stage' AS stage,
    (match_data->>'$.season.id')::INTEGER AS season_id,
    (match_data->>'$.homeTeam.id')::INTEGER AS home_team_id,
    match_data->>'$.homeTeam.name' AS home_team_name,
    match_data->>'$.homeTeam.tla' AS home_team_tla,
    (match_data->>'$.awayTeam.id')::INTEGER AS away_team_id,  
    match_data->>'$.awayTeam.name' AS away_team_name,  
    match_data->>'$.awayTeam.tla' AS away_team_tla,
    (match_data->>'$.score.fullTime.home')::INTEGER AS fulltime_home_goals,
    (match_data->>'$.score.fullTime.away')::INTEGER AS fulltime_away_goals,
    (match_data->>'$.score.halfTime.home')::INTEGER AS halftime_home_goals,
    (match_data->>'$.score.halfTime.away')::INTEGER AS halftime_away_goals,
    match_data->>'$.score.winner' AS winner,
    match_data->>'$.score.duration' AS duration
FROM
    matches