import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def test_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT')),
            database=os.getenv('DB_DATABASE'),
            user=os.getenv('DB_USERNAME'),
            password=os.getenv('DB_PASSWORD')
        )
        print("✅ PostgreSQL connection successful!")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()