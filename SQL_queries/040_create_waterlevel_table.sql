

/* Create table Waterlevel */

DROP TABLE public."Waterlevel";


CREATE TABLE public."Waterlevel"
(
    Sid varchar(4),
    Place varchar(50),
    Timestamp TIMESTAMP,
    Param varchar(4) NULL,
    Value decimal(10, 2) NULL
    
)
WITH (
    OIDS = FALSE
);


/*INSERT INTO public."Waterlevel" values ('20001 Fusternberg', TIMESTAMP '2023-03-19 12:30:00.123456', 326, 59.40);*/


