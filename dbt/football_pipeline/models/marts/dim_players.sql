SELECT DISTINCT
    player_id, 
    player_first_name, 
    player_last_name, 
    player_date_of_birth, 
    player_nationality
FROM
    {{ ref('stg_scorers') }}