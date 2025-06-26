import pymysql
from flask import jsonify

host_name = "localhost"
user_name = "root"
password = ""
schema_name = "dealer_db"


def execute_query(mysql_query, mode, *args):
    db_connection = pymysql.connect(
        host=host_name,
        user=user_name,
        passwd=password,
        database=schema_name
    )
    cursor = db_connection.cursor(pymysql.cursors.DictCursor)

    try:
        if mode == 'read':
            if not mysql_query.upper().startswith('SELECT'):
                return jsonify({'message': 'Only SELECT queries are allowed in read mode.'}), 400

            cursor.execute(mysql_query, args)
            data = cursor.fetchall()
            record_count = cursor.rowcount
            return jsonify({'message': f'{record_count} row(s) fetched successfully', 'data': data}), 200
        elif mode == 'write':
            if not mysql_query.upper().startswith('INSERT'):
                return jsonify({'message': 'Only INSERT queries are allowed in write mode.'}), 400
            cursor.execute(mysql_query, args)
            affected_rows = cursor.rowcount
            db_connection.commit()
            return jsonify({'message': f'{affected_rows} row(s) inserted successfully'}), 200
        else:
            return jsonify({'message': 'Invalid mode. Use \'read\' or \'write\'.'}), 400
    except Exception as e:
        cursor.close()
        db_connection.close()
        if mode == 'read':
            return jsonify({'message': 'Error in read operation. Check query syntax or permissions.'}), 500
        elif mode == 'write':
            return jsonify({'message': 'Error in write operation. Check query syntax or permissions.'}), 500
        else:
            return jsonify({'message': 'Error in query execution. Check query syntax or permissions.'}), 500

    finally:
        cursor.close()
        if db_connection.open:
            db_connection.close()
