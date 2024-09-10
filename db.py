import pymysql
import os
timeout = 10
def connect_to_db():
    connection = pymysql.connect(
    charset="utf8mb4",
    connect_timeout=timeout,
    cursorclass=pymysql.cursors.DictCursor,
    db=os.environ["DB"],
    host=os.environ["HOST"],
    password=os.environ["PASSWORD"],
    read_timeout=timeout,
    port=os.environ["DB_PORT"],
    user=os.environ["USER"],
    write_timeout=timeout,
    )
    return connection
#made a mistake in creating the db table 
#thats why the function might not make sense
def insert_feedback(answer, suggestion):
    connection = connect_to_db()
    
    try:
        with connection.cursor() as cursor:
            sql_insert = "INSERT INTO feedback2 (name, suggestion) VALUES (%s, %s)"
            cursor.execute(sql_insert, (answer, suggestion))
            connection.commit()  # Save changes
    finally:
        connection.close()
