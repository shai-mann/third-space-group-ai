CREATE OR REPLACE FUNCTION get_user_features(user_id integer)
RETURNS TABLE (
    age_difference integer,
    is_buddy integer,
    is_friend integer,
    common_friends_count integer,
    common_hobbies_count integer,
    common_groups_count integer
) AS $$
BEGIN
    -- Calculate age difference with the central user
    SELECT ABS(u.age - central.age) INTO age_difference
    FROM users u, users central
    WHERE u.id = user_id AND central.id = 0;

    -- Check if the user is a buddy with the central user and cast to integer
    SELECT (CASE WHEN u.buddy_id = 0 THEN 1 ELSE 0 END) INTO is_buddy
    FROM users u
    WHERE u.id = user_id;

    -- Check if the user is a friend with the central user and cast to integer
    SELECT (CASE WHEN EXISTS (
        SELECT 1 FROM user_friends uf WHERE uf."user" = user_id AND uf.friend = 0
    ) THEN 1 ELSE 0 END) INTO is_friend;

    -- Calculate the number of common friends with the central user
    SELECT COUNT(*) INTO common_friends_count
    FROM user_friends uf1
    JOIN user_friends uf2 ON uf1.friend = uf2.friend
    WHERE uf1."user" = user_id AND uf2."user" = 0;

    -- Get the count of common hobbies with the central user
    SELECT COUNT(*) INTO common_hobbies_count
    FROM (
        SELECT uh.hobby
        FROM user_hobbies uh
        WHERE uh."user" = user_id
        INTERSECT
        SELECT uh.hobby
        FROM user_hobbies uh
        WHERE uh."user" = 0
    ) AS common_hobbies;

    -- Get the count of common groups with the central user
    SELECT COUNT(*) INTO common_groups_count
    FROM (
        SELECT gm.group
        FROM group_members gm
        WHERE gm."user" = user_id
        INTERSECT
        SELECT gm.group
        FROM group_members gm
        WHERE gm."user" = 0
    ) AS common_groups;

    RETURN NEXT;
END; $$
LANGUAGE plpgsql;