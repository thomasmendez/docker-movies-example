-- Database: movies

DROP TABLE IF EXISTS films;

CREATE TABLE films (
    id          serial primary key,
    title       text NOT NULL,
    day         integer NOT NULL,
    month       integer NOT NULL,
    year        integer NOT NULL,
    file_data   bytea
);