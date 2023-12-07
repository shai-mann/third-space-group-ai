/*
This SQL script initializes the database schema for the application. It performs the following tasks:
1. Drops the existing 'admin' user and all objects owned by it.
2. Creates a new 'admin' user with superuser privileges and sets an encrypted password.
3. Grants all privileges on the 'postgres' database to the 'admin' user.
4. Grants all privileges on all tables and sequences in the 'public' schema to the 'admin' user.
5. Creates the 'users' table with columns for user information and a UUID primary key.
6. Creates the 'hobbies' table with columns for hobby information and an auto-incrementing integer primary key.
7. Creates the 'user_hobbies' table to establish a many-to-many relationship between users and hobbies.
8. Creates the 'user_friends' table to establish a many-to-many relationship between users and their friends.
9. Creates the 'groups' table with columns for group information and an auto-incrementing integer primary key.
10. Creates the 'group_members' table to establish a many-to-many relationship between groups and their members.
*/
-- DB init code - runs every time the app starts up

-- drop owned by admin;
-- drop user admin;

-- create user admin superuser encrypted password 'adminPassword';
-- grant all privileges on database postgres to admin;

-- grant all privileges on all tables in schema public to admin;
-- grant all privileges on all sequences in schema public to admin;

create table if not exists users (
    id integer,
    first_name text,
    primary key (id)
);

create table if not exists hobbies (
    id integer generated by default as identity,
    "name" text,
    primary key (id)
);

create table if not exists user_hobbies (
    id integer generated by default as identity,
    "user" integer,
    hobby integer,
    primary key (id),
    foreign key ("user") references users,
    foreign key (hobby) references hobbies
);

create table if not exists user_friends (
    id integer generated by default as identity,
    "user" integer,
    friend integer,
    primary key (id),
    foreign key ("user") references users,
    foreign key (friend) references users
);

CREATE TABLE IF NOT EXISTS user_affinities (
    id integer GENERATED BY DEFAULT AS IDENTITY,
    user_id integer NOT NULL,
    related_user_id integer NOT NULL,
    affinity_score integer NOT NULL DEFAULT 0,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (related_user_id) REFERENCES users(id),
    UNIQUE (user_id, related_user_id) 
);

create table if not exists groups (
    id integer generated by default as identity,
    conversation int,
    "name" text,
    description text,
    primary key (id)
);

create table if not exists group_members (
    id integer generated by default as identity,
    "user" integer,
    "group" integer,
    primary key (id),
    foreign key ("user") references users,
    foreign key ("group") references groups
);
