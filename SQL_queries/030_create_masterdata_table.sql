

/* Create table Sells */

DROP TABLE public."Masterdata";


CREATE TABLE public."Masterdata"
(
    Urlparamid numeric(4) PRIMARY KEY,
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



