/* 
  Connect as user env_master to database env_db:
  psql -h localhost -U env_master -d env_db -f 030_create_bars_exercise_tables_and_insert_V001.sql 
*/


/* Create table Sells */

/*DROP TABLE public."Stations";*/


/*CREATE TABLE public."Stations"
(
    Sid varchar(50),
    Name varchar(50),
    Peggelnummer decimal(10, 2),
    Geometry GEOMETRY(Point, 31466)
)
WITH (
    OIDS = FALSE
);*/


INSERT INTO public."Stations" values ('s6', 'Mengede, A45 ', 10026, '0101000020EA7A000000000000D0CB434100000000C1CE5541');


/*
INSERT INTO public."Sells" values ('Joes', 'Bud', 2.50);
INSERT INTO public."Sells" values ('Joes', 'Miller', 2.75);
INSERT INTO public."Sells" values ('Sues', 'Bud', 2.50);
INSERT INTO public."Sells" values ('Sues', 'Coors', 3.00);
*/


