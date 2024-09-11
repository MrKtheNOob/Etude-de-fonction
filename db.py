import pymysql
from dotenv import load_dotenv
import os
timeout = 10

def connect_to_db():
    connection = pymysql.connect(
    charset="utf8mb4",
    connect_timeout=timeout,
    cursorclass=pymysql.cursors.DictCursor,
    db=os.getenv("DB_NAME"),
    host=os.getenv("HOST"),
    password=os.getenv("PASSWORD"),
    read_timeout=timeout,
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    write_timeout=timeout,
    )
    return connection
#made a mistake in creating the db table 
#thats why the function might not make sense
def insert_feedback(answer, suggestion):
    load_dotenv()
    connection = connect_to_db()
    name=answer
    try:
        with connection.cursor() as cursor:
            sql_insert = "INSERT INTO feedback2 (name, suggestion) VALUES (%s, %s)"
            cursor.execute(sql_insert, (name, suggestion))
            connection.commit()  # Save changes
    finally:
        connection.close()    
    
