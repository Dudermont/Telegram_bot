select: dict = {
    'show_all': "SELECT * "
                "FROM users",
    'all_users': "SELECT * FROM users",
    'add_user': "INSERT INTO users (user_name) "
                "VALUES (%s)",
    'add_spend': "INSERT INTO operation (user_id, category, operation_value)"
                 " SELECT user_id, %s, %s "
                 "FROM users "
                 "WHERE user_name = %s",
    'all_spend': "SELECT SUM(operation_value) "
                 "FROM operation "
                 "INNER JOIN users USING(user_id) "
                 "WHERE user_name = %s",
    'category_spend': "SELECT SUM(operation_value) "
                      "FROM operation "
                      "INNER JOIN users USING(user_id) "
                      "WHERE user_name = %s  AND category = %s",
    'day_spend': "SELECT SUM(operation_value) "
                 "FROM operation "
                 "INNER JOIN users USING(user_id) "
                 "WHERE operation_date = %s "
                 "AND user_name = %s"

}
