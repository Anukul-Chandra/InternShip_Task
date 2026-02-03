import psycopg2

conn = psycopg2.connect(
    dbname="phones",
    user="anukulchandra",
    password="",  
    host="localhost",
    port="5432"
)

print("Database connected successfully")
