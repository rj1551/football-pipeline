SELECT
    id AS player_id,
    season_id,
    scorer_data->>'$.player.firstName' AS player_first_name,
    scorer_data->>'$.player.lastName' AS player_last_name,
    (scorer_data->>'$.player.dateOfBirth')::DATE AS player_date_of_birth,
    scorer_data->>'$.player.nationality' AS player_nationality,
    scorer_data->>'$.player.section' AS player_section,
    (scorer_data->>'$.player.shirtNumber')::INTEGER AS player_shirt_number,
    (scorer_data->>'$.team.id')::INTEGER AS team_id,
    scorer_data->>'$.team.name' AS team_name,
    scorer_data->>'$.team.tla' AS team_tla,
    (scorer_data->>'$.playedMatches')::INTEGER AS played_matches,
    COALESCE((scorer_data->>'$.goals')::INTEGER, 0) AS goals,
    COALESCE((scorer_data->>'$.assists')::INTEGER, 0) AS assists,
    COALESCE((scorer_data->>'$.penalties')::INTEGER, 0) AS penalties
FROM
    scorers