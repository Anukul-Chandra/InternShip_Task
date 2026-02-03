import psycopg2

conn = psycopg2.connect(
    dbname="phones",
    user="anukulchandra",
    password="",  
    host="localhost",
    port="5432"
)

print("Database connected successfully")

def fetch_phone_by_model(model_name):
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM samsung_phones WHERE model ILIKE %s",
        ('%' + model_name + '%',)
    )
    rows = cur.fetchall()
    cur.close()
    return rows

if __name__ == "__main__":
    result = fetch_phone_by_model("S23")
    print(result)

