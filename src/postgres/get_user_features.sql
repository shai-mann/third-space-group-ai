CREATE OR REPLACE FUNCTION get_user_features(user_id INTEGER, central_user_id INTEGER)
RETURNS TABLE (
    age_difference INTEGER,
    is_buddy INTEGER,
    is_friend INTEGER,
    common_friends_count INTEGER,
    common_hobbies_count INTEGER,
    common_groups_count INTEGER
) AS $$
BEGIN
    -- Calculate age difference with the central user
    SELECT ABS(u.age - central.age) INTO age_difference
    FROM users u, users central
    WHERE u.id = user_id AND central.id = central_user_id;

    -- Check if the user is a buddy with the central user and cast to integer
    SELECT (CASE WHEN u.buddy = central_user_id THEN 1 ELSE 0 END) INTO is_buddy
    FROM users u
    WHERE u.id = user_id;

    -- Check if the user is a friend with the central user and cast to integer
    SELECT (CASE WHEN EXISTS (
        SELECT 1 FROM friends f WHERE (f."user" = user_id AND f.friend = central_user_id) OR (f."user" = central_user_id AND f.friend = user_id)
    ) THEN 1 ELSE 0 END) INTO is_friend;

    -- Calculate the number of common friends with the central user
    SELECT COUNT(DISTINCT f1.friend) INTO common_friends_count
    FROM friends f1
    JOIN friends f2 ON f1.friend = f2.friend
    WHERE (f1."user" = user_id AND f2."user" = central_user_id) OR (f1."user" = central_user_id AND f2."user" = user_id);

    -- Get the count of common hobbies with the central user
    SELECT COUNT(DISTINCT uh.hobby) INTO common_hobbies_count
    FROM user_hobbies uh
    JOIN user_hobbies uh0 ON uh.hobby = uh0.hobby AND uh0."user" = central_user_id
    WHERE uh."user" = user_id;

    -- Get the count of common groups with the central user
    SELECT COUNT(DISTINCT gm.group) INTO common_groups_count
    FROM group_members gm
    JOIN group_members gm0 ON gm.group = gm0.group AND gm0."user" = central_user_id
    WHERE gm."user" = user_id;

    RETURN NEXT;
END; $$
LANGUAGE plpgsql;
