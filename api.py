import pymysql


def execute_query(mysql_query, mode, *args):
    host_name = "localhost"
    user_name = "root"
    password = ""
    schema_name = "dealer_db"

    db_connection = pymysql.connect(
        host=host_name,
        user=user_name,
        passwd=password,
        database=schema_name
    )
    cursor = db_connection.cursor(pymysql.cursors.DictCursor)
    if mode == 'read':
        cursor.execute(mysql_query, args)
        data = cursor.fetchall()
        cursor.close()
        db_connection.close()
        return data
    elif mode == 'write':
        try:
            cursor.execute(mysql_query, args)
        finally:
            db_connection.commit()
            cursor.close()
            db_connection.close()
            return f"Query Executed Successfully."
