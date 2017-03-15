create table if not exists registration (
    icao_code text primary key,
    registration text,
    created datetime
);

CREATE INDEX if not exists reg_idx on registration(icao_code);