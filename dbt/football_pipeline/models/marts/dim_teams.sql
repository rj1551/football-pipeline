SELECT DISTINCT 
    team_id, 
    team_name, 
    team_tla 
FROM 
    {{ ref('int_team_performance') }}