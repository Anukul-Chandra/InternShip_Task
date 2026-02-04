import psycopg2
from psycopg2.extras import DictCursor

# DB configuration settings
DB_CONFIG = {
    "dbname": "phones",
    "user": "anukulchandra",
    "password": "1234",
    "host": "localhost",
    "port": "5432"
}

# Connect to database safely
def get_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"❌ Database Connection Error: {e}")
        return None

# --- Function 1: Fetch Data ---
def fetch_phone_from_db(model_name: str):
    conn = get_connection()
    if not conn: return []
    
    cursor = conn.cursor(cursor_factory=DictCursor)
    
    
    query = """
        SELECT model, release_year, release_date, display,
               battery, camera, ram, storage, price
        FROM phones
        WHERE LOWER(model) LIKE %s
    """
    cursor.execute(query, (f"%{model_name.lower()}%",))
    rows = cursor.fetchall()
    
    formatted_rows = []
    for row in rows:
        formatted_rows.append((
            row['model'], row['release_year'], row['release_date'], 
            row['display'], row['battery'], row['camera'], 
            row['ram'], row['storage'], row['price']
        ))

    conn.close()
    return formatted_rows

#  Insert or Update Data 
def insert_phone_into_db(phone: dict):
    conn = get_connection()
    if not conn: return

    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO phones (
            model, release_year, release_date, display,
            battery, camera, ram, storage, price
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (model) DO UPDATE SET
            release_year = EXCLUDED.release_year,
            release_date = EXCLUDED.release_date,
            display = EXCLUDED.display,
            battery = EXCLUDED.battery,
            camera = EXCLUDED.camera,
            ram = EXCLUDED.ram,
            storage = EXCLUDED.storage,
            price = EXCLUDED.price;
        """
        
        cursor.execute(query, (
            phone["model"],
            phone.get("release_year", "Unknown"),
            phone.get("release_date", "Unknown"),
            phone.get("display", "Unknown"),
            phone.get("battery", "Unknown"),
            phone.get("camera", "Unknown"),
            phone.get("ram", "Unknown"),
            phone.get("storage", "Unknown"),
            phone.get("price", 0)
        ))
        
        conn.commit()
        print(f"✅ Saved/Updated DB: {phone['model']}")
        
    except Exception as e:
        print(f"❌ Insert Error: {e}")
        conn.rollback()
    finally:
        conn.close()