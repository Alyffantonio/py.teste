CREATE OR REPLACE VIEW fastest_lap_per_grand_prix AS
SELECT
    r.date AS "data da corrida",
    r.name AS "nome do grand prix",
    res.fastest_lap_time AS "tempo da volta mais rápida",
    d.full_name AS "nome completo do corredor",
    c.name AS "nome do construtor"
FROM
    results res
JOIN
    races r ON res.race_id = r.race_id
JOIN
    drivers d ON res.driver_id = d.driver_id
JOIN
    constructors c ON res.constructor_id = c.constructor_id
WHERE
    (res.race_id, res.fastest_lap_time) IN (
        SELECT
            sub.race_id,
            MIN(sub.fastest_lap_time)
        FROM
            results sub
        WHERE
            sub.fastest_lap_time IS NOT NULL
        GROUP BY
            sub.race_id
    )
ORDER BY res.fastest_lap_time ASC;



CREATE OR REPLACE VIEW racer_performance AS
SELECT
    y.year AS ano,
    f.full_name AS "nome completo do corredor",
    n.name AS "nome do construtor",
    COUNT(*) FILTER (WHERE res.position_order = 1) AS "total de vitórias",
    SUM(res.points) AS "total de pontos"
FROM
    results res
JOIN
    races y ON res.race_id = y.race_id
JOIN
    drivers f ON res.driver_id = f.driver_id
JOIN
    constructors n ON res.constructor_id = n.constructor_id
GROUP BY
    y.year, f.full_name, n.name
ORDER BY
    y.year, "total de vitórias" DESC;