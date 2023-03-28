/* 
  Connect as (U)ser postgres (superuser) to the maintence (d)atabase postgres:
  psql -h localhost -U postgres -d postgres 
*/

/* Environmental database env_db */

CREATE DATABASE groundwater
    WITH 
    OWNER = env_master
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;

COMMENT ON DATABASE env_db IS 'Environmental database.';

