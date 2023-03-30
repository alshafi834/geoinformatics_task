/* 
  Connect as user env_master to database env_db:
  psql -h localhost -U env_master -d env_db -f 030_create_bars_exercise_tables_and_insert_V001.sql 
*/


/* Create table Sells */

/*DROP TABLE public."Masterdata";*/


CREATE TABLE public."Masterdata"
(
    Urlparamid decimal(10, 2),
    Pegelnummer decimal(10, 2),
    Gewasser varchar(50) NULL,
    Flusskilometer decimal(10, 2) NULL,
    Pegelnullpunkt decimal(10, 2) NULL,
    Einzugsgebiet decimal(10, 2) NULL,
    Rechtswert decimal(10, 2) NULL,
    Hochwert decimal(10, 2) NULL,
    MHW decimal(10, 2) NULL,
    MW decimal(10, 2) NULL,
    MNW decimal(10, 2) NULL,
    Geometry GEOMETRY(Point, 31466)
)
WITH (
    OIDS = FALSE
);




/*INSERT INTO public."Masterdata" values (2, 20012, 'Lippe', 59.40, 50.13, 2656.00, 2622828.00, 5728949.00, 432, 337, 314);*/


/*
INSERT INTO public."Sells" values ('Joes', 'Bud', 2.50);
INSERT INTO public."Sells" values ('Joes', 'Miller', 2.75);
INSERT INTO public."Sells" values ('Sues', 'Bud', 2.50);
INSERT INTO public."Sells" values ('Sues', 'Coors', 3.00);
*/


