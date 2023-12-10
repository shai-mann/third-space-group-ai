-- DROPS ALL DATA IN THE DATABASE
-- This file exists in case a dev wants to reset their database

-- Drop the function first before dropping the tables
DROP FUNCTION IF EXISTS get_user_features(integer) CASCADE;

-- Drop tables in the reverse order of their dependencies
drop table if exists group_members CASCADE;
drop table if exists groups CASCADE;

drop table if exists user_hobbies CASCADE;
drop table if exists friends CASCADE;
drop table if exists affinities CASCADE;

-- Now you can safely drop the users table
drop table if exists users CASCADE;

-- Hobbies table does not have dependencies
drop table if exists hobbies CASCADE;
