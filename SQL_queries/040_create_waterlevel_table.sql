/* 
  Connect as user env_master to database env_db:
  psql -h localhost -U env_master -d env_db -f 030_create_bars_exercise_tables_and_insert_V001.sql 
*/


/* Create table Sells */

DROP TABLE public."Waterlevel";


CREATE TABLE public."Waterlevel"
(
    Sid varchar(50),
    Place varchar(50),
    Timestamp TIMESTAMP,
    Param varchar(50) NULL,
    Value decimal(10, 2) NULL
    
)
WITH (
    OIDS = FALSE
);


/*INSERT INTO public."Waterlevel" values ('20001 Fusternberg', TIMESTAMP '2023-03-19 12:30:00.123456', 326, 59.40);*/


/*
INSERT INTO public."Sells" values ('Joes', 'Bud', 2.50);
INSERT INTO public."Sells" values ('Joes', 'Miller', 2.75);
INSERT INTO public."Sells" values ('Sues', 'Bud', 2.50);
INSERT INTO public."Sells" values ('Sues', 'Coors', 3.00);
*/


