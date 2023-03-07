-- Database: mandle-py
DROP SCHEMA IF EXISTS public CASCADE;
DROP DATABASE IF EXISTS "mandle-py";

CREATE DATABASE "mandle-py"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8';

-- SCHEMA: public

\c mandle-py

CREATE SCHEMA IF NOT EXISTS public
    AUTHORIZATION postgres;

GRANT ALL ON SCHEMA public TO PUBLIC;

GRANT ALL ON SCHEMA public TO postgres;

-- Table: public shot

DROP TABLE IF EXISTS public."shot" CASCADE;

CREATE TABLE IF NOT EXISTS public."shot"
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name text COLLATE pg_catalog."default" NOT NULL,
    limits double precision Array[4],
    reso int Array[2] ,
    max_stability int,
    stabilities int[],
    CONSTRAINT shot_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."shot"
    OWNER to postgres;


\q