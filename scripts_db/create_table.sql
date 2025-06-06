
CREATE TABLE IF NOT EXISTS constructors (
    constructor_id  INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS drivers (
    driver_id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS races (
    race_id INTEGER PRIMARY KEY,
    year INTEGER NOT NULL,
    name TEXT NOT NULL,
    date DATE NOT NULL
);


CREATE TABLE IF NOT EXISTS results (
    result_id INTEGER PRIMARY KEY,
    race_id INTEGER NOT NULL,
    driver_id INTEGER NOT NULL,
    constructor_id INTEGER NOT NULL,
    position_order INTEGER NOT NULL,
    points INTEGER NOT NULL,
    fastest_lap_time TIME
);