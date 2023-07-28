SELECT
    user_id,
    group_name as user_group
FROM user
WHERE 1=1
    AND login="$login"
    AND password="$password"
