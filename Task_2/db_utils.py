import psycopg2

conn = psycopg2.connect(
    dbname="phones",
    user="anukulchandra",
    password="",
    host="localhost",
    port="5432"
)

def fetch_phone_from_db(keyword):
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM samsung_phones
        WHERE LOWER(model) LIKE %s
    """, ('%' + keyword.lower() + '%',))
    rows = cur.fetchall()
    cur.close()
    return rows

def insert_phone_into_db(phone):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO samsung_phones
        (model, release_date, display, battery, camera, ram, storage, price)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (model) DO NOTHING
    """, (
        phone["model"],
        phone["release_date"],
        phone["display"],
        phone["battery"],
        phone["camera"],
        phone["ram"],
        phone["storage"],
        phone["price"]
    ))
    conn.commit()
    cur.close()
