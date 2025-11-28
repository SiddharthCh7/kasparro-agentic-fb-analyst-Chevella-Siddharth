import os
import psycopg2

from dotenv import load_dotenv
load_dotenv()

def query_db(query: str):
    try:
        conn = psycopg2.connect(
            os.getenv("SUPABASE_URL")
        )
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
        return rows
    except Exception as e:
        return f"ERROR: Unable to fetch data: {e}"

def get_dates():
    try:
        conn = psycopg2.connect(
            os.getenv("SUPABASE_URL")
        )
        cur = conn.cursor()
        cur.execute("select min(date) as min_date, max(date) as max_date from campaigns_data;")
        rows = cur.fetchall()
        conn.close()
        return rows
    except Exception as e:
        return "min_date: 2025-01-01, max_date: 2025-03-31"