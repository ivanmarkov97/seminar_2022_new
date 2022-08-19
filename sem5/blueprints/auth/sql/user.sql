select u.name,
       u.group_name,
       ug.login group_login,
       ug.password group_password
from (select name,
             group_name
      from joom.user
      where 1
        and login='$login'
        and password='$password'
     ) u
left join joom.user_group ug
    on u.group_name = ug.name
