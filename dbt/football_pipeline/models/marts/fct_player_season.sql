SELECT
    player_season_id, 
    player_id, 
    season_id, 
    player_section, 
    player_shirt_number, 
    team_id, 
    played_matches, 
    goals, 
    assists, 
    penalties
FROM
    {{ ref('stg_scorers') }}