from fastapi import FastAPI
import psycopg2

app = FastAPI()

conn = psycopg2.connect(
    dbname="phones",
    user="anukulchandra",
    password="",
    host="localhost",
    port="5432"
)

def fetch_phone_by_model(model_name):
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM samsung_phones WHERE model ILIKE %s",
        ('%' + model_name + '%',)
    )
    rows = cur.fetchall()
    cur.close()
    return rows

@app.post("/ask")
def ask(question: str):
    if "S23" in question:
        data = fetch_phone_by_model("S23")
        return {"answer": data}

    if "S22" in question:
        data = fetch_phone_by_model("S22")
        return {"answer": data}

    return {"answer": "No matching Samsung phone found"}
