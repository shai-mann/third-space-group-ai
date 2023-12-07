-- add a default user
-- Insert Users
INSERT INTO users (id, first_name) VALUES
(0, 'Karim'), -- Central user
(1, 'James'), -- Buddy
(2, 'Amy'), -- Friend 1
(3, 'Bob'), -- Friend 2
(4, 'Alice'), -- Rando 1
(5, 'Tom'), -- Rando 2
(6, 'Lisa'); -- Rando 3


-- Insert Hobbies
INSERT INTO hobbies ("name") VALUES
('Tennis'),
('Chess'),
('Painting'),
('Soccer'),
('Reading'),
('Cycling');

-- These were added after the hobbies and the users were added through the extensions PostgresSQL
-- Replace the UUIDs with the actual UUIDs for each user
-- Replace the hobby IDs with the actual IDs for each hobby
-- If DB is reset, the UUIDs will change, so make sure to update them (Unless you assign the values manually)

-- Insert User Hobbies for Karim
INSERT INTO user_hobbies ("user", hobby) VALUES 
(0, 1), -- Tennis
(0, 2); -- Chess

-- Insert User Hobbies for James (Buddy)
INSERT INTO user_hobbies ("user", hobby) VALUES 
(1, 5), -- Reading
(1, 6); -- Cycling

-- Insert User Friends (Karim's friends Amy and Bob)
INSERT INTO user_friends ("user", friend) VALUES 
(0, 2), -- Amy
(0, 3); -- Bob

-- Insert User Affinities based on the relationships
-- Buddy (James) with high affinity score
INSERT INTO user_affinities (user_id, related_user_id, affinity_score) VALUES 
(0, 1, 100); -- James

-- Friends (Amy and Bob) with medium affinity score
INSERT INTO user_affinities (user_id, related_user_id, affinity_score) VALUES 
(0, 2, 50), -- Amy
(0, 3, 50); -- Bob


