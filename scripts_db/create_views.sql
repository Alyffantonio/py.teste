CREATE VIEW fastest_lap_per_grand_prix AS
SELECT
    r.date AS race_date,
    r.name AS grand_prix_name,
    res.fastest_lap_time AS fastest_lap_time,
    d.full_name AS driver_fullname,
    c.name AS constructor_name
FROM
    results res
JOIN races r ON res.race_id = r.race_id
JOIN drivers d ON res.driver_id = d.driver_id
JOIN constructors c ON res.constructor_id = c.constructor_id
WHERE
    res.fastest_lap_time IS NOT NULL AND
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
ORDER BY
    r.date DESC;



CREATE OR REPLACE VIEW resultado_corredores_por_ano AS
SELECT
    ra.year AS ano,
    dr.full_name AS nome_completo_corredor,
    co.name AS nome_construtor,
    COUNT(CASE WHEN re.position_order = 1 THEN 1 END) AS qtd_vitorias,
    SUM(re.points) AS qtd_pontos
FROM
    results re
JOIN races ra ON re.race_id = ra.race_id
JOIN drivers dr ON re.driver_id = dr.driver_id
JOIN constructors co ON re.constructor_id = co.constructor_id
GROUP BY
    ra.year, dr.full_name, co.name
ORDER BY
    ra.year, dr.full_name;