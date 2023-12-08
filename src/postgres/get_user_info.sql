CREATE OR REPLACE FUNCTION get_user_info(user_id integer)
RETURNS TABLE (
    returned_user_id integer,
    first_name text,
    age integer,
    buddy_id integer,
    hobby_name text,
    friend_id integer,
    friend_name text,
    group_id integer,
    group_name text
) AS $$
BEGIN
    RETURN QUERY 
    SELECT 
        u.id,
        u.first_name,
        u.age,
        u.buddy_id,
        h.name,
        uf.friend,
        uf2.first_name,
        g.id,
        g.name
    FROM 
        users u
    LEFT JOIN user_hobbies uh ON u.id = uh.user
    LEFT JOIN hobbies h ON uh.hobby = h.id
    LEFT JOIN user_friends uf ON u.id = uf.user
    LEFT JOIN users uf2 ON uf.friend = uf2.id
    LEFT JOIN group_members gm ON u.id = gm.user
    LEFT JOIN groups g ON gm.group = g.id
    WHERE 
        u.id = user_id;
END; $$
LANGUAGE plpgsql;
